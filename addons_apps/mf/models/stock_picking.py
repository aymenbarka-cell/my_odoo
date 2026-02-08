from odoo import fields, models,api
class stockPicking(models.Model):
    _inherit = 'stock.picking'
    remarque = fields.Text('Remarque')
    client_f=fields.Many2one('res.partner',string='Partenaire')
    @api.model_create_multi
    def create(self, vals_list):
        print(vals_list)
        res = super(stockPicking, self).create(vals_list)
        for vals in vals_list:
            order = self.env['sale.order'].search([('name','=',vals['origin'])])
            res.remarque = order.remarque
            res.client_f = order.client_f
        print(res.name)
        return res