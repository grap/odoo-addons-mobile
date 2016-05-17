# -*- coding: utf-8 -*-
# Copyright (C) 2016-Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv.orm import Model
from openerp.tools.translate import _


class PurchaseOrder(Model):
    _inherit = 'purchase.order'

    def create_order_by_scan(
            self, cr, uid, partner_id, context=None):
        value_obj = self.pool['ir.values']
        user_obj = self.pool['res.users']
        company = user_obj.browse(cr, uid, uid, context=context).company_id
        vals = self.default_get(
            cr, uid, self._defaults.keys(), context=context)
        vals.update({'partner_id': partner_id})
        vals.update({'warehouse_id': value_obj.get_default(
            cr, uid, 'purchase.order', 'warehouse_id', company_id=company.id)})

        vals.update(self.onchange_warehouse_id(
            cr, uid, False, vals.get('warehouse_id', False))['value'])
        vals.update(self.onchange_partner_id(
            cr, uid, False, partner_id)['value'])
        vals['origin'] = _("Barcode Reader")
        return super(PurchaseOrder, self).create(
            cr, uid, vals, context=context)

    def add_order_line_by_scan(
            self, cr, uid, id, product_id, qty, context=None):
        line_obj = self.pool['purchase.order.line']

        # Secure type before calling onchange_product_id func that doesn't
        # work with str value
        qty = float(qty)

        order = self.browse(cr, uid, id, context=context)
        uom_id = False
        pricelist_id = order.pricelist_id.id
        partner_id = order.partner_id.id
        line_vals = line_obj.onchange_product_id(
            cr, uid, False, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=order.date_order,
            fiscal_position_id=order.fiscal_position.id,
            date_planned=order.minimum_planned_date, name=False,
            price_unit=False, context=context)['value']
        line_vals.update({
            'product_id': product_id,
            'order_id': order.id,
        })
        # This framework is awsome
        line_vals['taxes_id'] = [[6, False, line_vals['taxes_id']]]
        order_vals = {'order_line': [[0, False, line_vals]]}
        return self.write(cr, uid, [id], order_vals, context=context)
