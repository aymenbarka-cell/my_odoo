from odoo import fields, models, api
from odoo.addons.test_convert.tests.test_env import record
from odoo.exceptions import UserError


class formationFormation(models.Model):
    _name = "formation.formation"
    _description = "Les formations"
    code=fields.Char(string="Formation Code")

    def print_report(self):
        return self.env.ref('mf.report_formation_salle').report_action(self)

    def validation(self):
        self.status = 'in'
        self.code = self.env['ir.sequence'].next_by_code('mf.formation')

    def cloturation(self):
        self.status = 'closed'

    @api.onchange("type_id")
    def onchange_type_id(self):
        self.description_f = self.type_id.description

    status = fields.Selection(selection=[('new', "à programmer"),
                                         ('in', "En cours"),
                                         ('closed', "Clôturé"), ], string="Status", default="new", required=False, )

    name = fields.Char(string="Nom de la formation", required=True)
    salle_id = fields.Many2one("formation.salle", string="la salle", domain="[('status', '=', 'libre')]")
    type_id = fields.Many2one("formation.type", string="le type")
    formateur_id = fields.Many2one("res.partner", string="le formateur", domain="[('formateur', '=', True)]",
                                   required=True)
    remarque=fields.Char(string="Remarque", groups="mf.formation_g2")
    description_f = fields.Char("type_id.description")
    # Il faut ajouter cette clé afin de lister les formations lines dans la vue
    formation_ligne_ids = fields.One2many('formation.formation.line', "formation_id")
    # Un champs compute veut dire qu'il est par défaut readonly et ne s'ajoute pas dateutilns la base de données
    note_g = fields.Integer("Moyenne", compute="_moyenne_note")

    @api.depends('formation_ligne_ids.note')
    def _moyenne_note(self):
        # print("  _moyenne_note", self)
        # for record in self:
        #     print("  _moyenne_note 2", record)
        #
        #     record.note_g=0
        for record in self:
            total = 0
            nb_empl = 0
            for empl in record.formation_ligne_ids:
                total += empl.note
                nb_empl += 1
            if total > 0:
                record.note_g = total / nb_empl
            else:
                record.note_g = 0

    date_debut = fields.Date(string="début de la formation")
    date_fin = fields.Date(string="Fin de la formation")

    @api.onchange('date_fin', 'date_debut')
    @api.constrains('date_fin', 'date_debut')
    def constrain_dates(self):
        for record in self:
            print(record)
            if record.date_debut and record.date_fin and record.date_debut > record.date_fin:
                raise UserError('Veuillez saisir une date de fin superieur à celle de début')

    def charger(self):
        self.formation_ligne_ids.unlink()
        employees = self.env['hr.employee'].search([])
        for employee in employees:
            self.env['formation.formation.line'].create({
                'formation_id' : self.id,
                'note' : 0,
                'employee_id' : employee.id
            })


class formationformationLine(models.Model):
    _name = "formation.formation.line"
    _description = "Les participants de la formation"

    employee_id = fields.Many2one('hr.employee', string="l'employee")
    note = fields.Integer("Note")
    formation_id = fields.Many2one('formation.formation', string="la formation")

    @api.onchange('note')
    @api.constrains('note')
    def constrain_note(self):
        for record in self:
            if record.note < 0 or record.note > 20:
                raise UserError('Veuillez donner une note entre 0 et 20')
