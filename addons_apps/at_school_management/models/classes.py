from odoo import models, fields, api, _
from datetime import date, datetime

class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'Class Record'

    name = fields.Char(string="Class Name", required=True)
    section = fields.Char(string="Section")
    grade = fields.Char(string="Grade")

    # Auto Academic Year
    academic_year = fields.Char(
        string="Academic Year",
        default=lambda self: f"{date.today().year}-{date.today().year + 1}",
        readonly=False
    )

    students = fields.Many2many(
        'school.student',
        'class_student_rel',       # relation table
        'class_id',                # column for this model
        'student_id',              # column for the related model
        string='Students'
    )

    # Class Type (user-creatable, like 'interchange', 'B2B', etc.)
    class_type_id = fields.Many2one('school.class.type', string="Class Type", required=True)

    # Monthly fee depending on type
    monthly_fee = fields.Float(string="Monthly Fee", related='class_type_id.monthly_fee', store=True)

    # Active flag and activation date (editable now)
    is_active = fields.Boolean(string="Active", default=False)
    activation_date = fields.Date(string="Activation Date", default=fields.Date.today)

    # Multiple study times (many2many for flexibility)
    study_time_ids = fields.Many2many(
        'school.study.time',
        string="Study Times",
        help="Define one or more study time slots for this class"
    )

    @api.onchange('is_active')
    def _onchange_is_active(self):
        """Automatically set activation date when activated."""
        for record in self:
            if record.is_active and not record.activation_date:
                record.activation_date = date.today()


class SchoolStudyTime(models.Model):
    _name = 'school.study.time'
    _description = 'Study Time Slot'

    name = fields.Char(string="Name", required=True)
    day_of_week = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ], string="Day of Week", required=True)

    start_time = fields.Float(string="Start Time (HH.MM)", required=True)
    end_time = fields.Float(string="End Time (HH.MM)", required=True)
