# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestModule(TransactionCase):

    def setUp(self):
        super(TestModule, self).setUp()
        self.wizard_obj = self.env['wizard.stock.inventory.merge']
        self.inventory_1 = self.env.ref('stock_inventory_merge.inventory_1')

    # Test Section
    def test_01_block_done_inventory(self):
        with self.assertRaises(UserError):
            self.inventory_1.action_done()

    def test_02_merge_duplicated_line(self):
        self.inventory_1.action_merge_duplicated_line()
        self.assertEqual(
            len(self.inventory_1.line_ids), 2,
            "Merging duplicated lines should delete lines.")
