from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DocumentArchive(models.Model):
    _name = 'document.archive'
    _description = 'Archived Document'

    name = fields.Char(string='Document Title', required=True)
    reference = fields.Char(string='Reference', required=True)
    date = fields.Date(string='Date', required=True)
    description = fields.Text(string='Description')
    category_id = fields.Many2one('document.category', string='Category')
    tag_ids = fields.Many2many('document.tag', string='Tags')

    # Full hierarchy — user can fill step by step
    direction_id = fields.Many2one('document.direction', string='Direction' , required=True)
    department_id = fields.Many2one(
        'document.department',
        string='Department',
        domain="[('direction_id', '=', direction_id)]"
       
    )
    section_id = fields.Many2one(
        'document.section',
        string='Section',
        domain="[('department_id', '=', department_id)]"
    )
    desk_id = fields.Many2one(
        'document.desk',
        string='Desk',
        domain="[('section_id', '=', section_id)]"
    )


    file = fields.Binary(string='File')
    file_name = fields.Char(string='File Name')

    # === HELPER FIELD FOR DASHBOARD COUNTING ===
    count_helper = fields.Integer(
        string='Count Helper',
        default=1,
        store=True  # ← Critical: must be stored
    )

    # ===== ONCHANGE: Auto-fill parents when child is selected (optional) =====
    @api.onchange('desk_id')
    def _onchange_desk_id(self):
        if self.desk_id:
            self.section_id = self.desk_id.section_id
            # Cascade up
            if self.section_id:
                self.department_id = self.section_id.department_id
                if self.department_id:
                    self.direction_id = self.department_id.direction_id

    @api.onchange('section_id')
    def _onchange_section_id(self):
        if self.section_id:
            self.department_id = self.section_id.department_id
            if self.department_id:
                self.direction_id = self.department_id.direction_id

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.direction_id = self.department_id.direction_id

    # ===== CONSTRAINT: Only the deepest field defines the archive level =====
    @api.constrains('direction_id', 'department_id', 'section_id', 'desk_id')
    def _check_location_consistency(self):
        for rec in self:
            # If desk is set, section/department/direction must match its path
            if rec.desk_id:
                if rec.section_id != rec.desk_id.section_id:
                    raise ValidationError(_("Section must match the desk's section."))
                if rec.department_id != rec.desk_id.section_id.department_id:
                    raise ValidationError(_("Department must match the desk's department."))
                if rec.direction_id != rec.desk_id.section_id.department_id.direction_id:
                    raise ValidationError(_("Direction must match the desk's direction."))
            elif rec.section_id:
                if rec.department_id != rec.section_id.department_id:
                    raise ValidationError(_("Department must match the section's department."))
                if rec.direction_id != rec.section_id.department_id.direction_id:
                    raise ValidationError(_("Direction must match the section's direction."))
            elif rec.department_id:
                if rec.direction_id != rec.department_id.direction_id:
                    raise ValidationError(_("Direction must match the department's direction."))
            elif rec.direction_id:
                # OK
                pass
            else:
                raise ValidationError(_("Please select at least a Direction to archive the document."))
    # Add these methods to your DocumentArchive class

@api.onchange('direction_id')
def _onchange_direction_id(self):
    if self.direction_id:
        return {
            'domain': {
                'department_id': [('direction_id', '=', self.direction_id.id)],
                'section_id': [('department_id.direction_id', '=', self.direction_id.id)],
                'desk_id': [('section_id.department_id.direction_id', '=', self.direction_id.id)]
            }
        }
    else:
        return {'domain': {
            'department_id': [],
            'section_id': [],
            'desk_id': []
        }}

@api.onchange('department_id')
def _onchange_department_id(self):
    if self.department_id:
        return {
            'domain': {
                'section_id': [('department_id', '=', self.department_id.id)],
                'desk_id': [('section_id.department_id', '=', self.department_id.id)]
            }
        }
    else:
        return {'domain': {
            'section_id': [],
            'desk_id': []
        }}

@api.onchange('section_id')
def _onchange_section_id(self):
    if self.section_id:
        return {
            'domain': {
                'desk_id': [('section_id', '=', self.section_id.id)]
            }
        }
    else:
        return {'domain': {'desk_id': []}}       
    
@api.model
def default_get(self, fields_list):
    res = super().default_get(fields_list)
    
    # Get user's first access rule
    access = self.env.user.document_access_ids[:1]
    if access:
        if access.direction_id:
            res['direction_id'] = access.direction_id.id
        elif access.department_id:
            res['department_id'] = access.department_id.id
        elif access.section_id:
            res['section_id'] = access.section_id.id
        elif access.desk_id:
            res['desk_id'] = access.desk_id.id
    
    return res 
            