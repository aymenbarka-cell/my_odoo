from odoo import  fields, models

class formationClass(models.Model):
    _name = "formation.salle"
    _description = "Les salles de  formation "

    def print_report(self):
        return  self.env.ref('mf_test.report_formation_salle').report_action(self)

    ref = fields.Char(string="Ref")
    name =fields.Char(" nom de la salle",required=True)
    nb_place = fields.Integer('Nombre de place dans la salle')
    date_creation = fields.Date("date d'inoguration")
    if_machine =fields.Boolean("Contient des  machines")
    type_class=fields.Selection([
        ('1', '1er étage'),
        ('2', '2em étage'),
        ('3', '3em étage'),
        ('4', '4em étage'),
        ('5', '5em étage')],string="étage")

    type_ids =fields.Many2many('formation.type',"id","id"
                               ,string="Les types autorisé")
    status = fields.Selection(
        selection=[ ('en_cours', "En cours de formation"),
            ('libre', "Libre"),
            ('maintenance', "En maintenance"), ],
        string="Statut", default='libre', help="Statut", required=False, )
    immo_ids =fields.One2many('formation.salle.immo',"salle_id")
    currency_id = fields.Many2one('res.currency',
        default=lambda self: self.env.company.currency_id, string="Currency" )

class formationsalleimmo(models.Model):
    _name = "formation.salle.immo"
    _description = ("Les immobilisation de la salle de formation"
                    " (produit , valeur,remarque lien vers lasalle) ")

    product_id =fields.Many2one('product.template',"le produit")
    valeur =fields.Monetary(" Valeur",
                            currency_field='currency_id',
                            )
    remarque =fields.Text(" Remarque")
    salle_id =fields.Many2one('formation.salle',"la salle")

    currency_id = fields.Many2one('res.currency',
        related='salle_id.currency_id',
        string="Currency",
    )