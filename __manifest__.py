# -*- coding: utf-8 -*-
{
    'name': 'Македонска Испратница/Приемница',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'QWeb print template за Испратница и Приемница',
    'description': """
Македонска Испратница/Приемница
================================

Модул за печатење на Испратница и Приемница во македонски формат.

Функционалности:
-----------------
* QWeb PDF template за stock.picking
* Формат базиран на стандардна македонска испратница
* Податоци за компанија (лого, адреса, даночен број)
* Купувач и Примател секции
* Табела со производи (без цени)
* Потписи: ИЗДАЛ / ПРИМИЛ / Овластено лице

Автор: ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица
Website: https://www.eskon.com.mk
    """,
    'author': 'ЕСКОН-ИНЖЕНЕРИНГ ДООЕЛ Струмица',
    'website': 'https://www.eskon.com.mk',
    'license': 'LGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'reports/delivery_note_reports.xml',
        'reports/delivery_note_templates.xml',
        'reports/delivery_note_with_prices_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
