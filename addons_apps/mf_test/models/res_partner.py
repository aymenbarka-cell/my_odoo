from odoo import  fields, models

class resPartnerFormation(models.Model):
    _inherit = "res.partner"

    formateur =fields.Boolean("Formateur ?")

    def affecter(self):
        self.country_id= self.env.ref('base.dz')
        self.currency_id= self.env.ref('base.DZD')
        print("button affecter")
        formations=self.env["formation.formation"].search([('formateur_id','=',self.id)])
        print(formations)
        noms_formation=""
        for formation in formations:
            noms_formation+=formation.name+" "
        self.comment=noms_formation

    def dupliquer(self):
        self.env["res.partner"].create(
            {
            'name' :  self.name + " (copier par le module)",
            'email' :  self.email
        }
        )
