from odoo import fields, models, api


class Employee(models.Model):
    _inherit = 'hr.employee'
    moyenne = fields.Float("Moyenne", compute="_moyenne_note")
    nbf = fields.Integer("Nombre de formations", compute="_moyenne_note")

    # api pour remplir le champ "moyenne" dans la vue avec le resultat calculé dans compute="_moyenne_note"
    @api.depends()
    def _moyenne_note(self):
        for employee in self:
            print (employee)
            formations = employee.env['formation.formation.line'].search([('employee_id', '=', employee.id)])
            total = 0
            nbf = 0
            for formation in formations:
                total+=formation.note
                nbf+=1
            if nbf != 0:
                employee.moyenne=total/nbf
            else:
                employee.moyenne=0
            employee.nbf=nbf

    def Affiche_formation(self):
        action=self.env.ref("mf.formation_formation_line_action").read()[0]
        print (action)
        action['domain'] =  [('employee_id', '=', self.id)]
        return action


    # @api.model_create_multi
    # def create(self, vals_list):
    #     print(vals_list)
    #     res = super(Employee, self).create(vals_list)
    #     return res