from odoo import models, fields

class CourrierArchive(models.Model):
    _name = "courrier.archive"
    _description = "Courrier Archive"

    courrier_id = fields.Many2one("courrier.courrier", string="Courrier", required=True, ondelete="cascade")
    department_id = fields.Many2one("hr.department", string="Department", required=True)
    desk_id = fields.Many2one("courrier.desk", string="Desk")
    archived_by = fields.Many2one("res.users", string="Archived By", default=lambda self: self.env.user)
    archive_date = fields.Datetime(string="Archive Date", default=fields.Datetime.now)
    note = fields.Text(string="Archive Notes")
