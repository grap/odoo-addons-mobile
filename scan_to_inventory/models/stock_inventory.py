# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields
from openerp.osv.orm import Model
from openerp.tools.translate import _


class StockInventory(Model):
    _inherit = 'stock.inventory'

    # Compute Section
    def compute_inventory_line_qty(
            self, cr, uid, ids, name, args, context=None):
        res = {}
        for inventory in self.browse(cr, uid, ids, context=context):
            res[inventory.id] = len(inventory.inventory_line_id)
        return res

    # Columns Section
    _columns = {
        'inventory_line_qty': fields.function(
            compute_inventory_line_qty, string='Lines Qty', type='integer'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        print vals
        return super(StockInventory, self).write(
            cr, uid, ids, vals, context=context)

    def create_by_scan(
            self, cr, uid, name, context=None):
        vals = self.default_get(
            cr, uid, self._defaults.keys(), context=context)
        vals.update({'name': _('[Barcode Reader] %s') % (name)})
        return super(StockInventory, self).create(
            cr, uid, vals, context=context)

    def add_inventory_line_by_scan(
            self, cr, uid, id, location_id, product_id, qty, context=None):
        qty = float(qty)
        product_obj = self.pool['product.product']
        inventory = self.browse(cr, uid, id, context=context)
        product = product_obj.browse(cr, uid, product_id, context=context)
        line_vals = {
            'location_id': location_id,
            'product_id': product_id,
            'product_uom': product.uom_id.id,
            'product_qty': qty,
        }
        inventory_vals = {'inventory_line_id': [[0, False, line_vals]]}
        return self.write(cr, uid, [id], inventory_vals, context=context)
