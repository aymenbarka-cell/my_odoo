from odoo import  fields, models

class formationType(models.Model):
    _name = "formation.type"
    _description ="la table qui contient les types de formation"

    ref = fields.Char(string='Référence de type')
    name=fields.Char("Nom de type", required=True)
    description=fields.Char("Déscription de type")
    date_creation=fields.Date("date ")