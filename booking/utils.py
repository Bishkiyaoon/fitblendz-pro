from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)

def send_confirmation_email(appointment):
    """Send confirmation email to customer"""
    try:
        subject = f"Appointment Confirmation - {appointment.service.name}"
        
        # Format time for display
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        # Email context
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
            'service_price': appointment.service.price,
            'service_duration': appointment.get_duration_display(),
        }
        
        # Render email templates
        html_content = render_to_string('booking/emails/appointment_confirmation.html', context)
        text_content = render_to_string('booking/emails/appointment_confirmation.txt', context)
        
        # Log email attempt
        logger.info(f"Attempting to send confirmation email to {appointment.email}")
        logger.info(f"Using SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
        logger.info(f"From: {settings.DEFAULT_FROM_EMAIL}")
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Confirmation email sent successfully to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send confirmation email: {e}")
        logger.error(f"Email settings - Host: {settings.EMAIL_HOST}, Port: {settings.EMAIL_PORT}, User: {settings.EMAIL_HOST_USER}")
        logger.exception("Full traceback for email error:")
        return False

def send_reminder_email(appointment):
    """Send reminder email for upcoming appointment"""
    try:
        subject = f"Appointment Reminder - {appointment.service.name}"
        
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
        }
        
        html_content = render_to_string('booking/emails/appointment_reminder.html', context)
        text_content = render_to_string('booking/emails/appointment_reminder.txt', context)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Reminder email sent to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send reminder email: {e}")
        return False

def send_cancellation_email(appointment):
    """Send cancellation email"""
    try:
        subject = f"Appointment Cancelled - {appointment.service.name}"
        
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
        }
        
        html_content = render_to_string('booking/emails/appointment_cancelled.html', context)
        text_content = render_to_string('booking/emails/appointment_cancelled.txt', context)
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Cancellation email sent to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send cancellation email: {e}")
        return False

def send_status_confirmation_email(appointment):
    """Send confirmation email when appointment status is changed to confirmed"""
    try:
        subject = f"Appointment Confirmed - {appointment.service.name}"
        
        # Format time for display
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        # Email context
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
            'service_price': appointment.service.price,
            'service_duration': appointment.get_duration_display(),
        }
        
        # Render email templates
        html_content = render_to_string('booking/emails/appointment_status_confirmed.html', context)
        text_content = render_to_string('booking/emails/appointment_status_confirmed.txt', context)
        
        # Log email attempt
        logger.info(f"Attempting to send status confirmation email to {appointment.email}")
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Status confirmation email sent successfully to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status confirmation email: {e}")
        return False

def send_status_cancellation_email(appointment):
    """Send cancellation email when appointment status is changed to cancelled"""
    try:
        subject = f"Appointment Cancelled - {appointment.service.name}"
        
        # Format time for display
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        # Email context
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
        }
        
        # Render email templates
        html_content = render_to_string('booking/emails/appointment_status_cancelled.html', context)
        text_content = render_to_string('booking/emails/appointment_status_cancelled.txt', context)
        
        # Log email attempt
        logger.info(f"Attempting to send status cancellation email to {appointment.email}")
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Status cancellation email sent successfully to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status cancellation email: {e}")
        return False

def send_status_completion_email(appointment):
    """Send completion email when appointment status is changed to completed"""
    try:
        subject = f"Appointment Completed - {appointment.service.name}"
        
        # Format time for display
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        # Email context
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
        }
        
        # Render email templates
        html_content = render_to_string('booking/emails/appointment_status_completed.html', context)
        text_content = render_to_string('booking/emails/appointment_status_completed.txt', context)
        
        # Log email attempt
        logger.info(f"Attempting to send status completion email to {appointment.email}")
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Status completion email sent successfully to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send status completion email: {e}")
        return False

def send_pending_appointment_email(appointment):
    """Send pending appointment email when appointment is first created"""
    try:
        subject = f"Appointment Request Submitted - {appointment.service.name}"
        
        # Format time for display
        formatted_time = appointment.time.strftime('%I:%M %p')
        
        # Email context
        context = {
            'appointment': appointment,
            'formatted_time': formatted_time,
            'service_name': appointment.service.name,
            'service_price': appointment.service.price,
            'service_duration': appointment.get_duration_display(),
        }
        
        # Render email templates
        html_content = render_to_string('booking/emails/appointment_pending.html', context)
        text_content = render_to_string('booking/emails/appointment_pending.txt', context)
        
        # Log email attempt
        logger.info(f"Attempting to send pending appointment email to {appointment.email}")
        
        # Send email
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.email],
            html_message=html_content,
            fail_silently=False,
        )
        
        logger.info(f"Pending appointment email sent successfully to {appointment.email} for appointment {appointment.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send pending appointment email: {e}")
        return False

def is_working_hours(date, time):
    """Check if given date and time are within working hours"""
    try:
        from .models import WorkingHours
        
        # Get day of week (0=Monday, 6=Sunday)
        day_of_week = date.weekday()
        
        # Get working hours for this day
        working_hours = WorkingHours.objects.filter(day=day_of_week).first()
        
        if not working_hours or not working_hours.is_open:
            return False
        
        # Check if time is within working hours
        if working_hours.open_time and working_hours.close_time:
            return working_hours.open_time <= time <= working_hours.close_time
        
        return False
        
    except Exception as e:
        logger.error(f"Error checking working hours: {e}")
        return False

def is_holiday(date):
    """Check if given date is a holiday"""
    try:
        from .models import Holiday
        
        # Check for exact date match
        holiday = Holiday.objects.filter(date=date).first()
        if holiday:
            return True
        
        # Check for recurring holidays (same month and day)
        month = date.month
        day = date.day
        
        recurring_holidays = Holiday.objects.filter(
            is_recurring=True,
            date__month=month,
            date__day=day
        )
        
        return recurring_holidays.exists()
        
    except Exception as e:
        logger.error(f"Error checking holiday: {e}")
        return False

def get_available_slots(date, service_duration=30):
    """Get available time slots for a given date"""
    try:
        from .models import WorkingHours, Appointment
        
        # Check if it's a holiday
        if is_holiday(date):
            return []
        
        # Get working hours for this day
        day_of_week = date.weekday()
        working_hours = WorkingHours.objects.filter(day=day_of_week).first()
        
        if not working_hours or not working_hours.is_open:
            return []
        
        # Generate time slots
        slots = []
        current_time = working_hours.open_time
        
        while current_time < working_hours.close_time:
            # Check if this slot conflicts with existing appointments
            slot_end = (datetime.combine(date, current_time) + 
                       timezone.timedelta(minutes=service_duration)).time()
            
            # Check for conflicts
            conflicts = Appointment.objects.filter(
                date=date,
                time__lt=slot_end,
                status__in=['pending', 'confirmed']
            )
            
            # Check if any appointment overlaps with this slot
            has_conflict = False
            for appt in conflicts:
                appt_end = (datetime.combine(date, appt.time) + 
                           timezone.timedelta(minutes=appt.duration)).time()
                if current_time < appt_end:
                    has_conflict = True
                    break
            
            if not has_conflict:
                slots.append(current_time.strftime('%H:%M'))
            
            # Move to next slot (30-minute intervals)
            current_time = (datetime.combine(date, current_time) + 
                           timezone.timedelta(minutes=30)).time()
        
        return slots
        
    except Exception as e:
        logger.error(f"Error getting available slots: {e}")
        return []

def format_phone_number(phone):
    """Format phone number for display"""
    try:
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, str(phone)))
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
        elif len(digits) > 11:
            return f"+{digits}"
        else:
            return phone
            
    except Exception as e:
        logger.error(f"Error formatting phone number: {e}")
        return phone

def validate_appointment_time(date, time, service_duration):
    """Validate if appointment time is available"""
    try:
        from .models import Appointment
        
        # Check if it's in the past
        if date < timezone.now().date():
            return False, "Cannot book appointments in the past"
        
        # Check if it's too far in the future
        if date > timezone.now().date() + timezone.timedelta(days=90):
            return False, "Cannot book appointments more than 90 days in advance"
        
        # Check working hours
        if not is_working_hours(date, time):
            return False, "Selected time is outside working hours"
        
        # Check holidays
        if is_holiday(date):
            return False, "Selected date is a holiday and we are closed"
        
        # Check for conflicts
        slot_end = (datetime.combine(date, time) + 
                   timezone.timedelta(minutes=service_duration)).time()
        
        conflicts = Appointment.objects.filter(
            date=date,
            time__lt=slot_end,
            status__in=['pending', 'confirmed']
        )
        
        for appt in conflicts:
            appt_end = (datetime.combine(date, appt.time) + 
                       timezone.timedelta(minutes=appt.duration)).time()
            if time < appt_end:
                return False, "This time slot conflicts with an existing appointment"
        
        return True, "Time slot is available"
        
    except Exception as e:
        logger.error(f"Error validating appointment time: {e}")
        return False, "Error validating appointment time"
