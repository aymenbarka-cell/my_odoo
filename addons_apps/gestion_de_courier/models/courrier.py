from odoo import models, fields, api

class Courrier(models.Model):
    _name = "courrier.courrier"
    _description = "Courrier"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Subject", required=True, tracking=True)
    reference = fields.Char(string="Reference", readonly=True, copy=False, tracking=True)
    type = fields.Selection([
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
        ('internal', 'Internal'),
    ], string="Type", required=True, default='incoming', tracking=True)
    priority = fields.Selection([
        ('urgent', 'Urgent'),
        ('normal', 'Normal'),
        ('low', 'Low'),
    ], string="Priority", default='normal', tracking=True)
    flux = fields.Selection([
        ('arrivee', 'Arrivée'),
        ('depart', 'Départ'),
        ('interne', 'Interne'),
    ], string="Flux")
    assigned_department_id = fields.Many2one('hr.department', string="Assigned Department", tracking=True)
    assigned_desk_id = fields.Many2one('courrier.desk', string="Assigned Desk")
    action = fields.Selection([
        ('execution', 'Exécution'),
        ('consultation', 'Consultation'),
        ('suite', 'Suite à donner'),
        ('information', 'Information'),
    ], string="Action")
    parent_id = fields.Many2one("courrier.courrier", string="Related Courrier")
    child_ids = fields.One2many("courrier.courrier", "parent_id", string="Replies")
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('archived', 'Archived'),
    ], default='draft', tracking=True)
    out_side_dispatching = fields.Boolean(string="Dispatched Outside", default=False)

    @api.model
    def create(self, vals):
        # Assign reference based on type
        if vals.get('reference'):
            # if provided, keep
            pass
        else:
            if vals.get('type') == 'incoming':
                vals['reference'] = self.env['ir.sequence'].next_by_code('courrier.incoming') or '/'
            elif vals.get('type') == 'outgoing':
                vals['reference'] = self.env['ir.sequence'].next_by_code('courrier.outgoing') or '/'
            else:
                vals['reference'] = self.env['ir.sequence'].next_by_code('courrier.internal') or '/'
        # If assigned_department not provided, try set from creator
        if not vals.get('assigned_department_id') and self.env.uid:
            user = self.env.user
            if getattr(user, 'department_id', False):
                vals['assigned_department_id'] = user.department_id.id
        rec = super(Courrier, self).create(vals)
        rec.message_post(body="Courrier créé: %s" % (rec.reference or ''))
        return rec

    def action_assign(self):
        for rec in self:
            rec.state = 'assigned'
            if rec.assigned_department_id:
                rec.message_post(body="Assigned to department: %s" % rec.assigned_department_id.name)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_archive(self):
        Archive = self.env['courrier.archive']
        for rec in self:
            Archive.create({
                'courrier_id': rec.id,
                'department_id': rec.assigned_department_id.id if rec.assigned_department_id else False,
                'desk_id': rec.assigned_desk_id.id if rec.assigned_desk_id else False,
                'note': 'Archived from state %s' % rec.state,
            })
            rec.state = 'archived'
            rec.message_post(body="Courrier archivé")
