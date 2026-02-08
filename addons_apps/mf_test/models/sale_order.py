from odoo import  fields, models

class saleOrdFormation(models.Model):
    _inherit = "sale.order"

    remarque =fields.Char("Remarque")
    client_f_id =fields.Many2one('res.partner',"Client final")

    # def action_confirm(self):
    #     res = super().action_confirm()
    #     for order in self:
    #         for picking in order.picking_ids:
    #             picking.remarque= order.remarque
    #             picking.client_f_id= order.client_f_id
    #     return res
