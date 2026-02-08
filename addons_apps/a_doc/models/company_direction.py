from odoo import models, fields

class CompanyDirection(models.Model):
    _name = 'document.direction'
    _description = 'Company Direction'

    name = fields.Char(string='Direction Name', required=True)
    code = fields.Char(string='Code')
    department_ids = fields.One2many('document.department', 'direction_id', string='Departments')