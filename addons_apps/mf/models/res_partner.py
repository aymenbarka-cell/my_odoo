from odoo import fields, models
class formationClass(models.Model):
    _inherit = 'res.partner'
    formateur = fields.Boolean('Formateur ?')
    def affecter(self):
        print("Boutton affecter")
        self.website=self.name
        self.country_id=self.env.ref('base.dz')
        self.currency_id =self.env.ref('base.DZD')

        # c'est l'equivalent d'un select * en sql
        # formations = self.env['formation.formation'].search([])
        # chercher seulement les formations du contact
        formations=self.env['formation.formation'].search([('formateur_id', '=', self.id)])
        print(formations)
        noms_formations=""
        for formation in formations:
            # print (formation.name)
            noms_formations+=formation.name+"\n"
        self.comment=noms_formations
    def dupliquer(self):
        self.env['res.partner'].create({
            'name':self.name+"(copier par le module)"
        })