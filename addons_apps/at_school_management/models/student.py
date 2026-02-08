from odoo import models, fields, api, _
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'school.student'
    _description = 'Student Record'

    name = fields.Char(string="Full Name", required=True)
    admission_no = fields.Char(
        string="Admission No",
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    dob = fields.Date(string="Date of Birth", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string="Gender", required=True)
    medical_history = fields.Text(string="Medical History")
    parent_id = fields.Many2one('school.parent', string="Parent/Guardian")
    class_id = fields.Many2one('school.class', string="Class")
    document_ids = fields.One2many('school.student.document', 'student_id', string="Documents")
    blood_group = fields.Selection([
        ('O-', 'O-'), ('O+', 'O+'), ('A-', 'A-'), ('A+', 'A+'),
        ('B-', 'B-'), ('B+', 'B+'), ('AB-', 'AB-'), ('AB+', 'AB+')
    ], string="Blood Group")
    is_student = fields.Boolean(string="Is Student", default=False)
    house_address = fields.Text(string="Home Address", required=True)
    doj = fields.Date(string="Date of Joining", required=True, default=fields.Date.context_today)
    trackskill = fields.Text(string="Track Skills")
    image_1920 = fields.Image(string="Student Photo", max_width=1920, max_height=1920, store=True)

    total_due = fields.Float(string="Total Due", compute="_compute_payment_info", store=False)
    total_paid = fields.Float(string="Total Paid", compute="_compute_payment_info", store=False)
    balance_due = fields.Float(string="Balance Due", compute="_compute_payment_info", store=False)

    _sql_constraints = [
        ('unique_admission_no', 'unique(admission_no)', 'Admission number must be unique!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('admission_no', _('New')) == _('New'):
            vals['admission_no'] = self.env['ir.sequence'].next_by_code('school.student') or _('New')
        return super(Student, self).create(vals)

    @api.depends('class_id', 'is_student')
    def _compute_payment_info(self):
        today = date.today()
        for student in self:
            total_due = 0
            total_paid = 0

            if student.is_student and student.class_id and student.class_id.is_active:
                activation_date = student.class_id.activation_date

                if activation_date:
                    months_elapsed = (today.year - activation_date.year) * 12 + (today.month - activation_date.month)
                    if today.day >= activation_date.day:
                        months_elapsed += 1
                    months_elapsed = max(months_elapsed, 0)

                    total_due = months_elapsed * (student.class_id.monthly_fee or 0)

                    payments = self.env['school.fee.payment'].search([('admission_no', '=', student.id)])
                    total_paid = sum(p.amount_paid for p in payments)

            student.total_due = total_due
            student.total_paid = total_paid
            student.balance_due = total_due - total_paid

    @api.constrains('is_student', 'class_id')
    def _check_class_required(self):
        for student in self:
            if student.is_student and not student.class_id:
                raise ValidationError(_("Class is required for a student who is active."))
