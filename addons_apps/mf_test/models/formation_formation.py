from odoo import  fields, models,api,_
from odoo.exceptions import  UserError
import logging

_logger = logging.getLogger(__name__)


class formationformation(models.Model):
    _name = "formation.formation"
    _inherit = ['mail.thread']
    _description = "Les formations "

    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.company.currency_id, string="Currency")
    cost =fields.Monetary(" Cout de la formation",
                            currency_field='currency_id',
                            )
    def validation(self):
        self.status='in'
        self.code =self.env['ir.sequence'].next_by_code('mf_test.formation')

    @api.onchange('type_id')
    def onchange_type_id(self):
        self.description_f=self.type_id.description

    status = fields.Selection(
        selection=[('new', "à programmer"),
                   ('in', "En  cours"),
                   ('closed', "Clôturé"), ],
        string="Statut", default='new', required=True, )

    date_deb = fields.Date("Debut de formation")
    date_fin = fields.Date("Fin de formation")
    name =fields.Char(" Nom de la formation",required=True,translate=True)
    code =fields.Char(" Référence formation",readonly=True)
    salle_id =fields.Many2one('formation.salle',"la salle",
                              domain="[('status','=','libre')]")
    type_id =fields.Many2one('formation.type',"le type")
    formateur_id =fields.Many2one('res.partner',"Le formateur",
                                  domain="[('formateur', '=', True)]",
                                  required=True,)
    description_f =fields.Char("description")
    remarque =fields.Text("Remarque",groups="mf_test.formation_g2")

    employee_ids =fields.One2many('formation.formation.line',"formation_id")
    note_g =fields.Integer(" Note",compute="_moyenne_note")

    def charger(self):
        self.employee_ids.unlink()
        employees=self.env['hr.employee'].search([])
        for employee in employees:
            self.env['formation.formation.line'].create(
                {'formation_id':self.id,
                 'note':0,
                 'employee_id':employee.id
                }
            )

    @api.depends('employee_ids.note')
    def _moyenne_note(self):
        for record in self:
            total=0
            nb_empl=0
            for empl in record.employee_ids:
                total+= empl.note
                nb_empl+=1
            if nb_empl>0:
                record.note_g=total/nb_empl
            else:
                record.note_g=0





class formationformationLine(models.Model):
    _name = "formation.formation.line"
    _description = "Les participants de la formation "

    employee_id =fields.Many2one('hr.employee',"l'employee")
    note =fields.Integer(" Note")
    formation_id =fields.Many2one('formation.formation',"la formation")
    cost_line =fields.Monetary(" Cout par employé",
                            currency_field='currency_id',
                               compute="calcul_cost"

                            )
    currency_id = fields.Many2one('res.currency',
        related='formation_id.currency_id',
        string="Currency",
    )
    @api.onchange('note')
    @api.constrains('note')
    def constrain_note(self):
        for record in self:
            if record.note<0 or record.note>20:
                raise UserError('veuillez donner une note entre 0 et 20')

    def affiche(self):
        action = self.ref("mf_test.formation_formation_line_action").read()[0]
        action['domain'] = [('employee_id', '=', self.employee_id.id)]
        action['display_name'] = _("Historique  des formations de %s", self.employee_id.name)
        return action

    @api.depends('formation_id.cost')
    def calcul_cost(self):
        for rec in self:
            if rec.formation_id.employee_ids:
                rec.cost_line=rec.formation_id.cost/len(rec.formation_id.employee_ids)
            else :
                rec.cost_line = 0