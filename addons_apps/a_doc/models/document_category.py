from odoo import models, fields

class DocumentCategory(models.Model):
    _name = 'document.category'
    _description = 'Document Category'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True)