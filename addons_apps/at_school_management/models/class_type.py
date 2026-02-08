from odoo import models, fields

class SchoolClassType(models.Model):
    _name = 'school.class.type'
    _description = 'Class Type'

    name = fields.Char(string="Type Name", required=True)
    description = fields.Text(string="Description")
    monthly_fee = fields.Float(string="Monthly Fee", required=True)
    active = fields.Boolean(default=True)
