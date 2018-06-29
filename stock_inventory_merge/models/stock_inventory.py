# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, fields, models
from openerp.exceptions import Warning as UserError


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    duplicates_qty = fields.Integer(
        string='Duplicates Quantity', compute='_compute_duplicates_qty')

    _INVENTORY_LINE_KEY_FIELDS = [
        'product_id', 'location_id', 'partner_id', 'package_id', 'prod_lot_id']

    # Compute Section
    @api.multi
    def _compute_duplicates_qty(self):
        for inventory in self:
            inventory.duplicates_qty = len(
                inventory._get_duplicated_line_ids())

    # Overload Section
    @api.multi
    def action_done(self):
        inventories = self.filtered(lambda x: x.duplicates_qty)
        if inventories:
            raise UserError(
                "You can not confirm '%s' because there are"
                " some duplicated lines." % (
                    ', '.join([x.name for x in inventories])))
        return super(StockInventory, self).action_done()

    # Action Section
    @api.multi
    def action_merge_duplicated_line(self):
        line_obj = self.env['stock.inventory.line']
        for inventory in self:
            line_group_ids = inventory._get_duplicated_line_ids()
            for line_ids in line_group_ids:
                for line_data in line_obj.search_read(
                        [('id', 'in', line_ids)],
                        ['product_qty', 'product_uom']):
                    pass
                    # TODO

    # Custom Section
    @api.multi
    def _get_duplicated_line_ids(self):
        self.ensure_one()
        check_dict = {}
        line_vals = self._get_inventory_line_vals()
        for line_val in line_vals:
            key = self._get_inventory_line_keys(line_val)
            if key in check_dict:
                check_dict[key].append(line_val['id'])
            else:
                check_dict[key] = ['id']
        duplicates_group_ids = []
        for k, v in check_dict.iteritems():
            if len(v) > 1:
                duplicates_group_ids.append(v)
        return duplicates_group_ids

    @api.multi
    def _get_inventory_line_vals(self):
        line_obj = self.env['stock.inventory.line']
        return line_obj.search_read(
            [('inventory_id', 'in', self.ids)],
            self._INVENTORY_LINE_KEY_FIELDS)

    @api.model
    def _get_inventory_line_keys(self, values):
        res = []
        for field in self._INVENTORY_LINE_KEY_FIELDS:
            res.append(values.get(field) and values.get(field)[0] or False)
        return str(res)
