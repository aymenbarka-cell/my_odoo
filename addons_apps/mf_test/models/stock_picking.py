from odoo import  fields, models,api

class stockPickingFormation(models.Model):
    _inherit = "stock.picking"

    remarque =fields.Char("Remarque")
    client_f_id =fields.Many2one('res.partner',"Client final")

    # @api.model_create_multi
    # def create(self, vals_list):
    #     res = super(stockPickingFormation, self).create(vals_list)
    #     for vals in vals_list:
    #         order=self.env['sale.order'].search([('name','=',vals['origin'])],limit=1)
    #         res.remarque=order.remarque
    #         res.client_f_id=order.client_f_id
    #     return res