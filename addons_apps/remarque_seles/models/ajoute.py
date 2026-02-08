from odoo import fields, models,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remarque = fields.Text(string="Remarque")

    # def action_confirm(self):
    #     res = super().action_confirm()
    #     for order in self:
    #         for picking in order.picking_ids:
    #             picking.remarque_bd = order.remarque
    #             #picking.client_f_id=order.client_f_id
    #             print(picking.name)
    #     return res

