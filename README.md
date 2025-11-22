# Macedonia - Stock Reports / Магацински Извештаи

Comprehensive stock picking reports for Macedonian businesses in Odoo 18.

## Overview / Преглед

This module provides professional PDF reports for various stock operations in Macedonian businesses, including:

- **ИСПРАТНИЦА** - Delivery Note (outgoing transfers)
- **ПРИЕМНИЦА** - Receipt Note (incoming transfers)
- **РЕВЕРС** - Equipment Loan Document (equipment lending)
- **ПОВРАТНИЦА** - Equipment Return Document (equipment returns)

## Features / Функционалности

### Report Types / Типови на извештаи

1. **Basic Reports** - Without prices (Без цени)
   - Испратница - for outgoing deliveries
   - Приемница - for incoming receipts
   - Реверс - for equipment loans
   - Повратница - for equipment returns

2. **Reports with Prices** - Including unit costs and totals (Со цени)
   - Испратница со Цени
   - Приемница со Цени
   - Реверс со Цени
   - Повратница со Цени

### Smart Document Type Detection / Паметна детекција

The module automatically detects the appropriate document type based on:
- Picking type code (outgoing/incoming)
- Picking type name (for Реверс and Повратница)
- Shows only relevant report options in Print menu

### Professional Macedonian Format / Професионален формат

- **Header**: Company information (logo, address, tax number/ЕДБ)
- **Document Info**: Number, date, origin with Code128 barcode
- **Parties**: Sender (ИСПРАЌАЧ) and Receiver (ПРИМАТЕЛ) sections
- **Products Table**: Item number, code, name, quantity, unit of measure
- **Price Columns** (optional): Unit price, total amount without VAT
- **Signatures**: Three signature areas - ИЗДАЛ / ПРИМИЛ / Овластено лице
- **Full UTF-8 Support**: Proper Cyrillic character rendering

## Technical Details / Технички детали

### Dependencies / Зависности

- `stock` - Odoo Stock/Inventory module
- `l10n_mk_reverse` - Macedonian equipment loan module (for Реверс operations)

### Files Structure / Структура на фајлови

```
l10n_mk_stock_reports/
├── __init__.py
├── __manifest__.py
├── README.md
└── reports/
    ├── stock_reports.xml           # Report actions and domains
    ├── stock_report_templates.xml  # QWeb templates (basic)
    └── stock_report_with_prices_templates.xml  # QWeb templates (with prices)
```

### Report Actions / Акции за извештаи

| Report Name | Domain Filter | Template |
|------------|---------------|----------|
| Испратница | `picking_type_id.code = 'outgoing'` | report_stock_picking_mk |
| Приемница | `picking_type_id.code = 'incoming'` | report_stock_picking_mk |
| Реверс | `picking_type_id.name ilike 'Реверс'` | report_stock_picking_mk |
| Повратница | `picking_type_id.name ilike 'Враќање'` | report_stock_picking_mk |
| Испратница со Цени | `picking_type_id.code = 'outgoing'` | report_stock_picking_mk_with_prices |
| Приемница со Цени | `picking_type_id.code = 'incoming'` | report_stock_picking_mk_with_prices |
| Реверс со Цени | `picking_type_id.name ilike 'Реверс'` | report_stock_picking_mk_with_prices |
| Повратница со Цени | `picking_type_id.name ilike 'Враќање'` | report_stock_picking_mk_with_prices |

## Installation / Инсталација

### Prerequisites / Предуслови

1. Install the `l10n_mk_reverse` module first (if using Реверс/Повратница features)
2. Ensure your Odoo instance supports Macedonian language (mk_MK)

### Install via Docker (Production)

```bash
# Update module list
docker exec -i odoo_server odoo shell -d eskon --no-http << 'EOF'
env['ir.module.module'].update_list()
env.cr.commit()
