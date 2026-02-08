from odoo import api, fields, models


class ProjectProductList(models.Model):
    _name = 'project.product.list'
    _description = 'Product List (catalog template)'

    name = fields.Char(string='Name', required=True)
    product_ids = fields.Many2many('product.product', string='Products')


class ProjectCostEstimate(models.Model):
    _name = 'project.cost.estimate'
    _description = 'Project Cost Estimate'

    name = fields.Char(string="Estimation Name", required=True, default='New Estimation')
    project_id = fields.Many2one('project.project', string="Project", required=True)
    product_list_id = fields.Many2one('project.product.list', string='Product List (Template)')
    line_ids = fields.One2many('project.cost.estimate.line', 'estimate_id', string="Cost Lines", copy=True)
    total_cost = fields.Float(string="Total Cost", compute='_compute_total_cost', store=True)

    @api.depends('line_ids.subtotal')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = sum(line.subtotal for line in rec.line_ids)

    @api.onchange('product_list_id')
    def _onchange_product_list(self):
        """Append products from selected product list into estimate lines (keep old lines)."""
        for rec in self:
            if not rec.product_list_id:
                continue
            new_lines_cmds = []
            existing_product_ids = rec.line_ids.mapped('product_id.id')
            for p in rec.product_list_id.product_ids:
                if p.id in existing_product_ids:
                    continue
                new_lines_cmds.append((0, 0, {
                    'product_id': p.id,
                    'quantity': 1.0,
                    'cost_price': p.standard_price or 0.0,
                }))
            if new_lines_cmds:
                # Keep existing lines (as (4, id) commands) and append the new (0,0,vals) commands
                existing_cmds = [(4, l.id) for l in rec.line_ids]
                rec.line_ids = existing_cmds + new_lines_cmds

    def action_open_add_from_template(self):
        """Open the wizard (modal) to pick a product list and add its products."""
        self.ensure_one()
        return {
            'name': 'Add from Product List',
            'type': 'ir.actions.act_window',
            'res_model': 'project.add.products.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_estimate_id': self.id},
        }

    def action_open_product_catalog(self):
        """Open the product selection wizard (catalog modal)."""
        self.ensure_one()
        return {
            'name': 'Select Products',
            'type': 'ir.actions.act_window',
            'res_model': 'project.select.products.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_estimate_id': self.id},
        }


class ProjectCostEstimateLine(models.Model):
    _name = 'project.cost.estimate.line'
    _description = 'Project Cost Estimate Line'

    estimate_id = fields.Many2one('project.cost.estimate', string="Estimate", required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", default=1.0)
    cost_price = fields.Float(string="Cost Price", readonly=False)
    subtotal = fields.Float(string="Subtotal", compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'cost_price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = (rec.quantity or 0.0) * (rec.cost_price or 0.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.cost_price = rec.product_id.standard_price or 0.0


class ProjectAddProductsWizard(models.TransientModel):
    _name = 'project.add.products.wizard'
    _description = 'Wizard to add products from a Product List to an Estimate'

    estimate_id = fields.Many2one('project.cost.estimate', string='Estimate', required=True)
    product_list_id = fields.Many2one('project.product.list', string='Product List')

    @api.onchange('product_list_id')
    def _onchange_product_list(self):
        # nothing needed here; selection is used when user presses Add
        return

    def action_add_from_template(self):
        self.ensure_one()
        if not self.product_list_id:
            return {'type': 'ir.actions.act_window_close'}
        template_products = self.product_list_id.product_ids
        existing_product_ids = self.estimate_id.line_ids.mapped('product_id.id')
        lines = self.env['project.cost.estimate.line']
        for p in template_products:
            if p.id in existing_product_ids:
                continue
            lines.create({
                'estimate_id': self.estimate_id.id,
                'product_id': p.id,
                'quantity': 1.0,
                'cost_price': p.standard_price or 0.0,
            })
        return {'type': 'ir.actions.act_window_close'}


class ProjectSelectProductsWizard(models.TransientModel):
    _name = 'project.select.products.wizard'
    _description = 'Wizard to select products from catalog and add to estimate'

    estimate_id = fields.Many2one('project.cost.estimate', string='Estimate', required=True)
    product_ids = fields.Many2many('product.product', string='Products')

    @api.onchange('product_ids')
    def _onchange_product_ids(self):
        # no extra logic on change
        return

    def action_add_selected(self):
        self.ensure_one()
        if not self.product_ids:
            return {'type': 'ir.actions.act_window_close'}
        existing_product_ids = self.estimate_id.line_ids.mapped('product_id.id')
        lines = self.env['project.cost.estimate.line']
        for p in self.product_ids:
            if p.id in existing_product_ids:
                continue
            lines.create({
                'estimate_id': self.estimate_id.id,
                'product_id': p.id,
                'quantity': 1.0,
                'cost_price': p.standard_price or 0.0,
            })
        return {'type': 'ir.actions.act_window_close'}


# Add project button to open estimates filtered by project
class Project(models.Model):
    _inherit = 'project.project'

    def action_view_project_cost_estimates(self):
        self.ensure_one()
        action = self.env.ref('project_cost_estimate.action_project_cost_estimate', raise_if_not_found=False)
        if not action:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Cost Estimates',
                'res_model': 'project.cost.estimate',
                'view_mode': 'list,form',
                'domain': [('project_id', '=', self.id)],
                'context': {'default_project_id': self.id},
            }
        result = action.read()[0]
        result['domain'] = [('project_id', '=', self.id)]
        result['context'] = {'default_project_id': self.id}
        return result
