from odoo import models, fields
class formationReport(models.TransientModel):
    _name = 'formation.report'
    _description = 'Formation Report des formations'
    date_from = fields.Date(string='Du')
    date_to = fields.Date(string='Au')