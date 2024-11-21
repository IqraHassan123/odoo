from odoo import fields, models, api
from datetime import datetime

class BreakSchedule(models.Model):
    _name = "break.schedule"
    _description = "Break Schedule"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=False, ondelete='cascade', index=True)
    start_time = fields.Datetime(string='Start Time', required=False)
    end_time = fields.Datetime(string='End Time', required=False)
    type = fields.Selection(
        string='Break Type', selection=[
            ('prayer', 'Prayer'), ('lunch', 'Lunch'),
        ]
    )
    break_hours = fields.Float(string="Break Hours", compute="_compute_break_hours")

    @api.depends('start_time', 'end_time')
    def _compute_break_hours(self):
        for record in self:
            if record.start_time and record.type:
                # Determine the end time to use for calculation
                end_time = record.end_time if record.end_time else fields.Datetime.now()

                # Calculate duration between start_time and end_time
                duration = end_time - record.start_time
                break_seconds = duration.total_seconds()
                record.break_hours = break_seconds / 3600  # Convert seconds to hours

                # Logging to verify calculations
                if record.end_time:
                    print("=====> Calculated Break Hours with End Time:", record.break_hours)
                else:
                    print("=====> Calculated Ongoing Break Hours:", record.break_hours)

            else:
                # Reset to 0 if start_time or type is not set
                record.break_hours = 0.0

            # @api.depends('check_in','check_out','lunch_start', 'lunch_end','prayer_start','prayer_end')
    # def _compute_worked_hours(self):
    #     for record in self:
    #         if record.check_in and record.check_out:
    #              total_duration = record.check_out - record.check_in
    #              lunch_duration = timedelta(hours=record.lunch_hours)
    #              prayer_duration = timedelta(hours=record.prayer_hours)
    #              net_duration = total_duration - lunch_duration - prayer_duration
    #              record.worked_hours = net_duration.total_seconds() / 32400  #convert hours into sec/ total worked hours 9
    #         else:
    #             record.worked_hours = 0.0
    #
    # @api.depends('lunch_start', 'lunch_end', 'prayer_start', 'prayer_end')
    # def _compute_break_durations(self):
    #     for record in self:
    #
    #         if record.lunch_start and record.lunch_end:
    #             lunch_duration = record.lunch_end - record.lunch_start
    #             record.lunch_hours = lunch_duration.total_seconds() / 3600
    #         else:
    #             record.lunch_hours = 0.0
    #
    #         if record.prayer_start and record.prayer_end:
    #             prayer_duration = record.prayer_end - record.prayer_start
    #             record.prayer_hours = prayer_duration.total_seconds() / 1800
    #         else:
    #             record.prayer_hours = 0.0