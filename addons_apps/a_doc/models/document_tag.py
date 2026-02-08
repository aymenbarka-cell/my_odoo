from odoo import models, fields

class DocumentTag(models.Model):
    _name = 'document.tag'
    _description = 'Document Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color Index')  # For colored tags in UI
    active = fields.Boolean(default=True)