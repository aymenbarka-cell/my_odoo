from odoo import models, fields

class DocumentDesk(models.Model):
    _name = 'document.desk'
    _description = 'Desk'

    name = fields.Char(string='Desk Name', required=True)
    code = fields.Char(string='Code')
    section_id = fields.Many2one('document.section', string='Section', required=True)
    document_ids = fields.One2many('document.archive', 'desk_id', string='Documents')