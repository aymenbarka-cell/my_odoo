from odoo import fields, models, api

class HrEmployeeFormation(models.Model):
    _inherit = "hr.employee"

    moyenne = fields.Float(string="Moyenne", compute="_compute_moyenne", store=True)
    nbf = fields.Integer(string="Nombre de Formations", compute="_compute_moyenne", store=True)

    @api.depends('id')
    def _compute_moyenne(self):
        for employee in self:
            formations = self.env['formation.formation.line'].search([('employee_id', '=', employee.id)])
            total = 0
            nbf = len(formations)
            for formation in formations:
                total += formation.note or 0
            employee.moyenne = total / nbf if nbf else 0
            employee.nbf = nbf
