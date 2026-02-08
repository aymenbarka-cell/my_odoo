from odoo import fields, models
class devis(models.Model):
    _inherit = 'sale.order'
    remarque = fields.Text('Remarque')
    client_f=fields.Many2one('res.partner',string='Partner')
    def action_confirm(self):
        res=super().action_confirm()
        for order in self:
            for picking in order.picking_ids:
                # print(picking)
                picking.remarque = order.remarque
                picking.client_f = order.client_f
        return res
