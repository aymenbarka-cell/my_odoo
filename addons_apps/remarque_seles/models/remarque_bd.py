from odoo import models, api

class StockPickingFormation(models.Model):
    _inherit = 'stock.picking'

    # @api.model_create_multi
    # def create(self, vals_list):
    #     print("\n🔹 Creating Stock Picking with values:", vals_list)
    #     res = super(StockPickingFormation, self).create(vals_list)
    #
    #     for record, vals in zip(res, vals_list):
    #         origin = vals.get('origin')
    #         if origin:
    #             # Find the sale order that created this picking
    #             order = self.env['sale.order'].search([('name', '=', origin)], limit=1)
    #             if order:
    #                 record.remarque_bd = order.remarque
    #                 # Only assign if the field exists in stock.picking
    #                 if hasattr(record, 'client_f_id') and hasattr(order, 'client_f_id'):
    #                     record.client_f_id = order.client_f_id
    #
    #                 print(f"✅ Copied remarque from order {order.name} to picking {record.name}")
    #     return res
