from odoo import models, fields

class typeFormation(models.Model):
    _name = 'type.formation'
    _description = 'Type Formation'

    name = fields.Char(string='Nom de type de formation', required=True)
    description = fields.Char(string='Description de type de formation')