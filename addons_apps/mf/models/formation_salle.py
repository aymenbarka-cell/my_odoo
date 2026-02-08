from odoo import fields, models, api


class formationSalle(models.Model):
    _name = "formation.salle"
    _description = "la table qui contient les salles de formation"

    def Liberer(self):
        self.status = 'libre'

    def Maintenance(self):
        self.status = 'maintenance'

    ref = fields.Char(string='Référence de la salle')
    name = fields.Char("Nom de la salle", required=True)
    nb_place = fields.Integer("Nombre de places dans la salle")
    date_creation = fields.Date("date d'inoguration")
    if_machine = fields.Boolean("Contient des machine")
    type_class = fields.Selection([
        ('1', '1er etage') ,
        ('2', '2ene etage'),
        ('3', '3eme etage'),
        ('4', '4eme etage'),
        ('5', '5eme etage')], string='Etage')
    type_ids = fields.Many2many("formation.type", "id", "id", string="Les types autorisés")
    status = fields.Selection([('en_cours', "En cours de formation"),
                               ('libre', "libre"),
                               ('maintenance', "En maintenance")],
                              string="Statut", default="en_cours", help="Status", required=False)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id, string="Currency")

    salle_immo_ids = fields.One2many('formation.salle.immo', "salle_id")
    somme = fields.Monetary("Somme", compute="_somme_valeur")

    @api.depends('salle_immo_ids.valeur_p')
    def _somme_valeur(self):
        for record in self:
            total = 0
            for prod in record.salle_immo_ids:
                total += prod.valeur_p
            if total > 0:
                record.somme = total
            else:
                record.somme = 0


class formationSalleImmo(models.Model):
    _name = "formation.salle.immo"
    _description = "la table qui contient les equipement de la salle (produit, valeur, remarque, lien vers la salle)"

    produit_id = fields.Many2one("product.template", string="produit")

    valeur_p = fields.Monetary("Valeur", required=True)
    remarque = fields.Text("Remarque")
    salle_id = fields.Many2one("formation.salle", "Salle", required=True)
    currency_id = fields.Many2one('res.currency', related='salle_id.currency_id', string="Currency")
