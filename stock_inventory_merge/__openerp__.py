# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Stock - Merge Inventories',
    'summary': 'Allow to merge multiples partial inventories',
    'version': '8.0.1.0.0',
    'category': 'Stock',
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'stock',
    ],
    'data': [
        'views/view_stock_inventory_line.xml',
        'views/view_stock_inventory.xml',
        'views/view_wizard_stock_inventory_merge.xml',
    ],
    'demo': [
        'demo/res_groups.xml',
    ],
    'installable': True,
}
