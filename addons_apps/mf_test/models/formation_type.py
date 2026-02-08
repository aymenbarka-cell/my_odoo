from odoo import  fields, models

# création de la table type de formation


class formationType(models.Model):
    _name = "formation.type"
    _description = "Les types de formations (theme)"

    name =fields.Char(" Type",required=True)
    description =fields.Char(" Description")
