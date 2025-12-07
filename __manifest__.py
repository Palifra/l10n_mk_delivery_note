# -*- coding: utf-8 -*-
{
    'name': 'Macedonia - Stock Reports / Магацински Извештаи',
    'version': '18.0.2.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Macedonian stock picking reports: Испратница, Приемница, Реверс, Повратница',
    'description': """
Macedonia - Stock Reports / Магацински Извештаи
=================================================

Comprehensive stock picking reports for Macedonian businesses.

Supported Documents / Поддржани документи:
-------------------------------------------
* **ИСПРАТНИЦА** - Delivery Note (outgoing transfers)
* **ПРИЕМНИЦА** - Receipt Note (incoming transfers)
* **РЕВЕРС** - Equipment Loan Document (equipment lending)
* **ПОВРАТНИЦА** - Equipment Return Document (equipment returns)

Features / Функционалности:
-----------------------------
* QWeb PDF templates for stock.picking model
* Automatic document type detection based on picking type
* Smart Print menu - shows only relevant document type
* Professional Macedonian business format
* Company information (logo, address, tax number)
* Sender/Receiver sections with full details
* Product table with quantities and units
* Optional cost pricing variant
* Signature areas: ИЗДАЛ / ПРИМИЛ / Овластено лице
* Code128 barcode generation for document numbers
* Full UTF-8 support for Cyrillic characters

Report Variants / Варијанти на извештаи:
------------------------------------------
1. **Basic Report** - Without prices (Испратница/Приемница)
2. **With Prices** - Including unit costs and totals (со Цени)

Author: ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица
Website: https://www.eskon.com.mk
    """,
    'author': 'ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица',
    'website': 'https://www.eskon.com.mk',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'eskon_reverse',
    ],
    'data': [
        'reports/stock_reports.xml',
        'reports/stock_report_templates.xml',
        'reports/stock_report_with_prices_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
