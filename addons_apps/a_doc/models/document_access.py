from odoo import models, fields

class DocumentUserAccess(models.Model):
    _name = 'document.user.access'
    _description = 'User Document Access'

    user_id = fields.Many2one('res.users', string='User', required=True, ondelete='cascade')
    
    # Location (only one)
    direction_id = fields.Many2one('document.direction', string='Direction')
    department_id = fields.Many2one('document.department', string='Department')
    section_id = fields.Many2one('document.section', string='Section')
    desk_id = fields.Many2one('document.desk', string='Desk')
    
    # ✅ NEW: Allowed categories for this access rule
    category_ids = fields.Many2many('document.category', string='Allowed Categories')
    
    # Ensure only one location is set
    _sql_constraints = [
        ('check_single_location', 
         "CHECK((direction_id IS NOT NULL)::int + (department_id IS NOT NULL)::int + (section_id IS NOT NULL)::int + (desk_id IS NOT NULL)::int = 1)",
         "Please assign exactly one location.")
    ]
    # Add this field to DocumentUserAccess model
    permission_level = fields.Selection([
       ('read', 'Read Only'),
       ('write', 'Read & Write')
    ], string='Permission Level', default='read', required=True)