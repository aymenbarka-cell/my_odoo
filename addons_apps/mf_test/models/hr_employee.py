from odoo import  fields, models,api,_

class hrEmployeeFormation(models.Model):
    _inherit = "hr.employee"

    moyenne =fields.Float("Moyenne",compute="calcul_moyenne")
    nbf =fields.Integer("Nombre de formation",compute="calcul_moyenne")

    def affiche_formation(self):
        action = self.env.ref("mf_test.formation_formation_line_action").read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        return action

    @api.depends()
    def calcul_moyenne(self):
        for employee in self:
            formations=employee.env['formation.formation.line'].search([('employee_id','=',employee.id)])
            total=nbf=0
            for formation in formations:
                total+=formation.note
                nbf+=1
            if nbf !=0:
                employee.moyenne=total/nbf
            else:
                employee.moyenne=0
            employee.nbf = nbf

