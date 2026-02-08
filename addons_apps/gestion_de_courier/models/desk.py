from odoo import models, fields

class CourrierDesk(models.Model):
    _name = "courrier.desk"
    _description = "Desk / Bureau in Department"

    name = fields.Char(string="Desk Name", required=True)
    department_id = fields.Many2one("hr.department", string="Department", required=True)
    user_ids = fields.Many2many("res.users", string="Desk Members")
