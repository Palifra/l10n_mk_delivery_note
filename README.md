# Macedonian Delivery Note / Македонска Испратница

Odoo 18 module for printing Delivery Notes (Испратница/Приемница) in Macedonian format.

## Features

- **Two Report Types:**
  - **Испратница/Приемница** - Basic delivery note without prices
  - **Испратница/Приемница со Цени** - Delivery note with cost prices (standard_price)

- **Document Elements:**
  - Company information box with VAT number (ЕДБ)
  - Document title (ИСПРАТНИЦА for outgoing, ПРИЕМНИЦА for incoming)
  - Document number and date
  - Code128 barcode for document number
  - Sender (ИСПРАЌАЧ) and Receiver (ПРИМАТЕЛ) sections
  - Product table with: line number, product code, name, quantity, unit of measure
  - Optional: unit cost price and line amount (without VAT)
  - Notes section
  - Signature fields: ИЗДАЛ (Issued by), ПРИМИЛ (Received by), Овластено лице (Authorized person)

- **Technical Features:**
  - Uses `web.external_layout` for Bootstrap CSS and standard header/footer
  - DejaVu Sans font for proper Cyrillic character support
  - Responsive layout using Bootstrap grid system
  - Automatic language detection based on partner language
  - Clean table borders with proper styling

## Installation

1. Copy the `l10n_mk_delivery_note` folder to your Odoo addons directory
2. Update the module list in Odoo
3. Install "Македонска Испратница/Приемница" from Apps menu

### Docker Installation

```bash
# Update module list
docker exec -i odoo_server odoo shell -d YOUR_DATABASE --no-http << 'EOF'
env['ir.module.module'].update_list()
env.cr.commit()
EOF

# Install module
docker exec -i odoo_server odoo shell -d YOUR_DATABASE --no-http << 'EOF'
module = env['ir.module.module'].search([('name', '=', 'l10n_mk_delivery_note')])
module.button_immediate_install()
env.cr.commit()
EOF
```

## Usage

1. Go to **Inventory > Operations > Transfers**
2. Open any stock picking (delivery order or receipt)
3. Click **Print** button
4. Select either:
   - **Испратница/Приемница** - for basic delivery note
   - **Испратница/Приемница со Цени** - for delivery note with cost prices

The report automatically detects:
- **Outgoing** transfers → printed as "ИСПРАТНИЦА" (Delivery Note)
- **Incoming** transfers → printed as "ПРИЕМНИЦА" (Receipt Note)
- **Реверс** operations → printed as "РЕВЕРС" (Equipment Loan)
- **Враќање на Реверс** operations → printed as "ПОВРАТНИЦА" (Equipment Return)

**Note:** The Print menu shows only the relevant document type based on the picking operation.

## Screenshots

The generated PDF includes:
- Company logo and information (from external_layout)
- Document header with barcode
- Sender and receiver information
- Product details table
- Signature areas

## Dependencies

- `stock` (Odoo Inventory module)
- `l10n_mk_reverse` (Equipment Loan Management - for Реверс/Повратница support)

## Technical Details

- **Models:** stock.picking
- **Reports:** QWeb PDF templates
- **Version:** 18.0.1.0.0
- **License:** LGPL-3

### File Structure

```
l10n_mk_delivery_note/
├── __init__.py
├── __manifest__.py
├── README.md
├── reports/
│   ├── __init__.py
│   ├── delivery_note_reports.xml      # Report actions
│   ├── delivery_note_templates.xml    # Basic template (no prices)
│   └── delivery_note_with_prices_templates.xml  # Template with prices
└── tests/
    ├── __init__.py
    └── test_delivery_note_report.py   # Unit tests
```

## Customization

### Changing Fonts
Edit the `<style>` section in template files to use different fonts:
```xml
<style>
    body {
        font-family: Your Font, sans-serif !important;
    }
</style>
```

### Adjusting Layout
Modify column widths in the product table by changing the `width` percentages in `<th>` tags.

### Adding Fields
To add custom fields to the report, edit the template XML files and use QWeb directives like `t-field` or `t-esc`.

## Testing

Run the included tests:

```bash
./odoo-bin -d YOUR_DATABASE -u l10n_mk_delivery_note --test-enable --test-tags=/l10n_mk_delivery_note --stop-after-init
```

Tests cover:
- Report action registration
- PDF generation for outgoing/incoming transfers
- Multiple products
- Multiple pickings
- Barcode generation
- Notes rendering

## Changelog

### Version 18.0.1.1.0
- Added conditional report menu based on picking type
- Added support for РЕВЕРС and ПОВРАТНИЦА documents
- Added l10n_mk_reverse as dependency
- Improved document type detection

### Version 18.0.1.0.0
- Initial release
- Basic delivery note template (ИСПРАТНИЦА/ПРИЕМНИЦА)
- Delivery note with cost prices
- Full Macedonian language support
- Code128 barcode generation
- Comprehensive test suite

## Support

For issues and feature requests, please create an issue on GitHub.

## Author

**ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица**

- Website: https://www.eskon.com.mk
- Email: info@eskon.com.mk
- GitHub: https://github.com/Palifra

## Related Modules

- [l10n_mk](https://github.com/Palifra/l10n_mk) - Macedonian Chart of Accounts
- [l10n_mk_reverse](https://github.com/Palifra/l10n_mk_reverse) - Equipment Loan Management

## License

This module is licensed under LGPL-3.
