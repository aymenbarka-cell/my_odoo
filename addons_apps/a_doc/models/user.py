# models/user.py
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    document_access_ids = fields.One2many('document.user.access', 'user_id', string='Document Access')
    
    # ✅ Computed fields for security rule
    allowed_direction_ids = fields.Many2many('document.direction', compute='_compute_allowed_locations')
    allowed_department_ids = fields.Many2many('document.department', compute='_compute_allowed_locations')
    allowed_section_ids = fields.Many2many('document.section', compute='_compute_allowed_locations')
    allowed_desk_ids = fields.Many2many('document.desk', compute='_compute_allowed_locations')
    allowed_category_ids = fields.Many2many('document.category', compute='_compute_allowed_locations')

    def _compute_allowed_locations(self):
        for user in self:
            access = user.document_access_ids
            user.allowed_direction_ids = access.direction_id
            user.allowed_department_ids = access.department_id
            user.allowed_section_ids = access.section_id
            user.allowed_desk_ids = access.desk_id
            user.allowed_category_ids = access.category_ids