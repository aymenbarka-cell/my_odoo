# models/section.py
from odoo import models, fields

class DocumentSection(models.Model):
    _name = 'document.section'
    _description = 'Document Section'

    name = fields.Char(string='Section Name', required=True)
    code = fields.Char(string='Section Code')
    
    # Link to parent: Department
    department_id = fields.Many2one(
        'document.department',
        string='Department',
        required=True,
        ondelete='cascade'
    )
    
    # Link to children: Desks
    desk_ids = fields.One2many(
        'document.desk',
        'section_id',
        string='Desks'
    )