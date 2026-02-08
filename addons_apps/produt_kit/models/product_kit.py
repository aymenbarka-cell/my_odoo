from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_kit = fields.Boolean(string="Is a Kit?", default=False)
    kit_line_ids = fields.One2many("product.kit.line", "kit_id", string="Kit Components")
    kit_total_cost = fields.Float(string="Kit Total Cost", compute="_compute_kit_total_cost", store=True)

    @api.depends("kit_line_ids.subtotal")
    def _compute_kit_total_cost(self):
        for product in self:
            if product.is_kit:
                total = sum(line.subtotal for line in product.kit_line_ids)
                product.kit_total_cost = total
                product.standard_price = total  # 🔑 update product cost
            else:
                product.kit_total_cost = 0.0
                

    kit_available_qty = fields.Float(
    string="Available Quantity (Kit)",
    compute="_compute_kit_available_qty",
    store=False
    )

    @api.depends("kit_line_ids.product_id", "kit_line_ids.quantity")
    def _compute_kit_available_qty(self):
        for product in self:
            if product.is_kit and product.kit_line_ids:
                qtys = []
                for line in product.kit_line_ids:
                    if line.quantity > 0 and line.product_id.exists():
                        available = line.product_id.qty_available / line.quantity
                        qtys.append(available)
                product.kit_available_qty = min(qtys) if qtys else 0.0
            else:
                product.kit_available_qty = 0.0


class ProductKitLine(models.Model):
    _name = "product.kit.line"
    _description = "Product Kit Line"

    kit_id = fields.Many2one("product.template", string="Kit Product", ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Component", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    unit_cost = fields.Float(string="Unit Cost", compute="_compute_unit_cost", store=False, readonly=True)
    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends("product_id")
    def _compute_unit_cost(self):
        for line in self:
            line.unit_cost = line.product_id.standard_price or 0.0

    @api.depends("quantity", "unit_cost")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_cost
