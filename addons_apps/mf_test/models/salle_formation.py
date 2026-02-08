from odoo import models, fields, api


class salleFormation(models.Model):
    _name = 'salle.formation'
    _description = 'Model pour la class salle formation'

    ref = fields.Char(string='Ref de la salle de formation')
    name = fields.Char(string='Nom de la salle de formation', required=True)
    nb_place = fields.Integer(string='Nombre des palce disponible dans la salle de formation', required=True)
    created_date = fields.Date(string='Date creation')
    if_machine = fields.Boolean(string='machine exist')
    type_class = fields.Selection([
        ('1', '1er Etage'),
        ('2', '2er Etage'),
        ('3', '3er Etage'),
        ('4', '4er Etage'),
        ('5', '5er Etage'),
    ])
    status = fields.Selection(
        selection=[('libre', "Salle Libre"), ('en_cours', "En cours de formation"),
                   ('maintenance', "En maintenance"), ],
        string="Status",
        default="libre",
        help="Status",
        required=False)

    type_formation = fields.Many2many('type.formation', "id", "id", string="Formation autorisé")
    immob_ids = fields.One2many('salle.formation.immobilier', 'salle_id', string="Immobilier de la salle de formation")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id,
                                  string="Currency")

    total_valeurs = fields.Monetary(string="Valeur totale",
                                    compute="_compute_total_valeurs",
                                    currency_field="currency_id")

    @api.depends('immob_ids')
    def _compute_total_valeurs(self):
        for record in self:
            record.total_valeurs = sum(record.immob_ids.mapped('valeur')) if record.immob_ids else 0.0


class SalleFormationImmobilier(models.Model):
    _name = 'salle.formation.immobilier'
    _description = "l'immobilier des salle formation"

    salle_id = fields.Many2one('salle.formation', string='Salle')
    remarque = fields.Text(string='Description')
    product_ids = fields.Many2one('product.template', string='Products')
    valeur = fields.Monetary(string='Valeur', currency_field='currency_id')

    currency_id = fields.Many2one('res.currency', related="salle_id.currency_id", string='Currency')
