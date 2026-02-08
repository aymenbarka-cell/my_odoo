from odoo import models, fields

class DocumentDepartment(models.Model):
    _name = 'document.department'
    _description = 'Department'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Code')
    direction_id = fields.Many2one('document.direction', string='Direction', required=True)
    section_ids = fields.One2many('document.section', 'department_id', string='Sections')