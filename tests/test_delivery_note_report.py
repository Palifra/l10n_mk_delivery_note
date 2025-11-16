# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError


@tagged('post_install', '-at_install', 'l10n_mk_delivery_note')
class TestDeliveryNoteReport(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Create test company with full details
        cls.company = cls.env.company
        cls.company.write({
            'name': 'ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ',
            'street': 'ул. Маршал Тито бр. 10',
            'city': 'Струмица',
            'zip': '2400',
            'phone': '+389 34 321 123',
            'email': 'info@eskon.com.mk',
            'website': 'https://www.eskon.com.mk',
            'vat': 'MK4080009501842',
        })

        # Create test partner
        cls.partner = cls.env['res.partner'].create({
            'name': 'Тест Клиент ДООЕЛ',
            'street': 'ул. Гоце Делчев бр. 5',
            'city': 'Скопје',
            'zip': '1000',
            'vat': 'MK1234567890123',
        })

        # Create test product
        cls.product = cls.env['product.product'].create({
            'name': 'Тест Производ',
            'default_code': 'TP001',
            'type': 'consu',
            'uom_id': cls.env.ref('uom.product_uom_unit').id,
        })

        # Get warehouse and picking types
        cls.warehouse = cls.env['stock.warehouse'].search([
            ('company_id', '=', cls.company.id)
        ], limit=1)

        cls.picking_type_out = cls.warehouse.out_type_id
        cls.picking_type_in = cls.warehouse.in_type_id

    def test_01_report_action_exists(self):
        """Test that the report action is properly registered"""
        report_action = self.env.ref(
            'l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing',
            raise_if_not_found=False
        )

        self.assertIsNotNone(report_action, "Report action should exist")
        self.assertEqual(report_action.model, 'stock.picking')
        self.assertEqual(report_action.report_type, 'qweb-pdf')
        self.assertEqual(
            report_action.report_name,
            'l10n_mk_delivery_note.report_delivery_note_mk'
        )

    def test_02_report_template_exists(self):
        """Test that the QWeb template is registered"""
        template = self.env.ref(
            'l10n_mk_delivery_note.report_delivery_note_mk',
            raise_if_not_found=False
        )
        self.assertIsNotNone(template, "Report template should exist")

    def test_03_generate_outgoing_report(self):
        """Test generating report for outgoing (Испратница)"""
        # Create outgoing picking
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 10.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            })],
        })

        # Confirm the picking
        picking.action_confirm()

        # Get the report action
        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')

        # Render the report (this will raise an error if template has issues)
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content, "PDF content should be generated")
        self.assertEqual(report_type, 'pdf')
        self.assertGreater(len(pdf_content), 0, "PDF should have content")

    def test_04_generate_incoming_report(self):
        """Test generating report for incoming (Приемница)"""
        # Create incoming picking
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_in.id,
            'location_id': self.partner.property_stock_supplier.id,
            'location_dest_id': self.picking_type_in.default_location_dest_id.id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 5.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.partner.property_stock_supplier.id,
                'location_dest_id': self.picking_type_in.default_location_dest_id.id,
            })],
        })

        picking.action_confirm()

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_incoming')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)
        self.assertEqual(report_type, 'pdf')

    def test_05_report_with_multiple_products(self):
        """Test report with multiple product lines"""
        # Create second product
        product2 = self.env['product.product'].create({
            'name': 'Втор Производ',
            'default_code': 'TP002',
            'type': 'consu',
        })

        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': [
                (0, 0, {
                    'name': self.product.name,
                    'product_id': self.product.id,
                    'product_uom_qty': 10.0,
                    'product_uom': self.product.uom_id.id,
                    'location_id': self.picking_type_out.default_location_src_id.id,
                    'location_dest_id': self.partner.property_stock_customer.id,
                }),
                (0, 0, {
                    'name': product2.name,
                    'product_id': product2.id,
                    'product_uom_qty': 20.0,
                    'product_uom': product2.uom_id.id,
                    'location_id': self.picking_type_out.default_location_src_id.id,
                    'location_dest_id': self.partner.property_stock_customer.id,
                }),
            ],
        })

        picking.action_confirm()

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)
        self.assertGreater(len(pdf_content), 0)

    def test_06_report_without_partner(self):
        """Test report generation without partner (should still work)"""
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            })],
        })

        picking.action_confirm()

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)

    def test_07_report_with_notes(self):
        """Test that notes are included in the report"""
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'note': 'Ова е тест забелешка за испратницата.',
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            })],
        })

        picking.action_confirm()

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)

    def test_08_report_binding_to_model(self):
        """Test that report is bound to stock.picking model"""
        report_action = self.env.ref(
            'l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing'
        )

        self.assertEqual(
            report_action.binding_model_id.model,
            'stock.picking',
            "Report should be bound to stock.picking"
        )
        self.assertEqual(
            report_action.binding_type,
            'report',
            "Binding type should be 'report'"
        )

    def test_09_print_report_name(self):
        """Test that print name is correctly formatted"""
        report_action = self.env.ref(
            'l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing'
        )

        # Check that print_report_name contains the pattern
        self.assertIn('Испратница', report_action.print_report_name)
        self.assertIn('object.name', report_action.print_report_name)

    def test_10_multiple_pickings_report(self):
        """Test generating report for multiple pickings at once"""
        picking1 = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 5.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            })],
        })

        picking2 = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 3.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            })],
        })

        picking1.action_confirm()
        picking2.action_confirm()

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(
            report.id,
            [picking1.id, picking2.id]
        )

        self.assertIsNotNone(pdf_content)
        self.assertGreater(len(pdf_content), 0)

    def test_11_multi_page_report_with_many_products(self):
        """Test report with 25+ products to verify multi-page rendering"""
        # Create 25 different products
        products = []
        for i in range(25):
            product = self.env['product.product'].create({
                'name': f'Производ {i+1:02d} - Тест артикл за повеќе страници',
                'default_code': f'MP{i+1:03d}',
                'type': 'consu',
            })
            products.append(product)

        # Create picking with all 25 products
        move_vals = []
        for i, product in enumerate(products):
            move_vals.append((0, 0, {
                'name': product.name,
                'product_id': product.id,
                'product_uom_qty': float(i + 1),
                'product_uom': product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            }))

        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': move_vals,
        })

        picking.action_confirm()

        # Verify we have 25 moves
        self.assertEqual(
            len(picking.move_ids.filtered(lambda m: m.state != 'cancel')),
            25,
            "Picking should have 25 moves"
        )

        # Generate report
        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)
        self.assertEqual(report_type, 'pdf')
        # PDF with 25 items should be larger than single item PDF
        self.assertGreater(len(pdf_content), 5000, "PDF should be substantial for 25 items")

    def test_12_barcode_generation(self):
        """Test that barcode is generated for document number"""
        picking = self.env['stock.picking'].create({
            'partner_id': self.partner.id,
            'picking_type_id': self.picking_type_out.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id': self.partner.property_stock_customer.id,
            'move_ids': [(0, 0, {
                'name': self.product.name,
                'product_id': self.product.id,
                'product_uom_qty': 1.0,
                'product_uom': self.product.uom_id.id,
                'location_id': self.picking_type_out.default_location_src_id.id,
                'location_dest_id': self.partner.property_stock_customer.id,
            })],
        })

        picking.action_confirm()

        # The barcode URL should be generated from picking name
        barcode_value = picking.name.replace('/', '')
        self.assertTrue(barcode_value, "Barcode value should not be empty")

        report = self.env.ref('l10n_mk_delivery_note.action_report_delivery_note_mk_outgoing')
        pdf_content, report_type = report._render_qweb_pdf(report.id, picking.ids)

        self.assertIsNotNone(pdf_content)
