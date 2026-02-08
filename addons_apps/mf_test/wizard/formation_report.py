from odoo import fields,models
import base64

class formationReport(models.TransientModel):
    _name = 'formation.report'
    _description = 'Rapports des formations'

    date_from = fields.Date("Du",required=1)
    date_to = fields.Date("Au",required=1)
    department_id = fields.Many2one("hr.department", string="Département")

    file_data = fields.Binary(string="Fichier TXT",readonly=True)
    file_name = fields.Char(default="liste_employes.txt")

    def generate_pdf(self):
        return  self.env.ref('mf_test.report_formation_report').report_action(self)
    def generate_txt(self):
        if self.department_id:
            line_formation = self.env['formation.formation.line'].search([
                ("employee_id.department_id",'=',self.department_id.id),
                ("formation_id.date_fin",'>',self.date_from),
                ("formation_id.date_fin",'<',self.date_to),            ])
        else:
            line_formation = self.env['formation.formation.line'].search([
                ("formation_id.date_fin",'>',self.date_from),
                ("formation_id.date_fin",'<',self.date_to),
            ])
        employees=line_formation.mapped("employee_id")
        content =""
        for empl in employees:
            content+="\n"+empl.name
        self.file_data = base64.b64encode(content.encode('utf-8'))
        self.file_name ="employes.txt"
        return {    'type': 'ir.actions.act_window',
            'res_model': 'formation.report',
            'res_id': self.id,
            'view_mode': 'form',
            'target':'new'        }


    def get_formation(self):
        line_formation = self.env['formation.formation.line'].search([
            ("employee_id.department_id", '=', self.department_id.id),
            ("formation_id.date_fin", '>', self.date_from),
            ("formation_id.date_fin", '<', self.date_to), ])
        formations=line_formation.mapped("formation_id")
        dict={}
        for formation in formations:
            cout_d=0
            for line in formation.employee_ids:
              if line.employee_id.department_id == self.department_id:
                cout_d+=line.cost_line
            dict.update({formation.name:cout_d})
        print(dict)
        return formations



