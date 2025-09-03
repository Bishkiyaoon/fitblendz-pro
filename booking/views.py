from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta
import json
import logging
# from django_ratelimit.decorators import ratelimit  # Temporarily disabled due to installation issues
from .models import Appointment, Service, WorkingHours, Holiday
from .webhook_views import send_appointment_notification
from .utils import send_pending_appointment_email, send_status_confirmation_email, send_status_cancellation_email, send_status_completion_email, is_working_hours, is_holiday

logger = logging.getLogger(__name__)

def home(request):
    """Home page with services and booking form"""
    try:
        services = Service.objects.filter(is_active=True).order_by('name')
        context = {
            'services': services,
            'page_title': 'FitBlendz Pro - Professional Barber Services'
        }
        return render(request, 'booking/home.html', context)
    except Exception as e:
        logger.error(f"Error in home view: {e}")
        messages.error(request, "Sorry, there was an error loading the page. Please try again.")
        return render(request, 'booking/error.html', {'error': str(e)})

def admin_login(request):
    """Custom admin login page"""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('booking:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('booking:admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'booking/admin_login.html', {
        'page_title': 'Admin Login - FitBlendz Pro'
    })

def admin_logout(request):
    """Admin logout view"""
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    return redirect('booking:admin_login')

def booking_page(request):
    """Booking page with appointment form"""
    try:
        if request.method == "GET":
            appt_id = request.GET.get("appt")
            services = Service.objects.filter(is_active=True).order_by('name')
            
            context = {
                'services': services,
                'appointment_id': appt_id,
                'today_date': timezone.now().date().isoformat(),
                'page_title': 'Book Your Appointment - FitBlendz Pro'
            }
            return render(request, 'booking/booking.html', context)
        
        elif request.method == "POST":
            return handle_booking_submission(request)
            
    except Exception as e:
        logger.error(f"Error in booking_page view: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while processing your request. Please try again.'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
# @ratelimit(key='ip', rate='5/m', method='POST', block=True)  # Temporarily disabled due to installation issues
def handle_booking_submission(request):
    """Handle booking form submission"""
    try:
        # Extract and validate form data
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'service', 'date', 'time']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }, status=400)
        
        # Validate service
        try:
            service = Service.objects.get(id=data['service'], is_active=True)
        except Service.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Selected service is not available'
            }, status=400)
        
        # Validate date and time
        try:
            appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            appointment_time = datetime.strptime(data['time'], '%H:%M').time()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid date or time format'
            }, status=400)
        
        # Check if appointment is in the past
        if appointment_date < timezone.now().date():
            return JsonResponse({
                'success': False,
                'error': 'Cannot book appointments in the past'
            }, status=400)
        
        # Check if appointment is in the future (within reasonable time)
        if appointment_date > timezone.now().date() + timedelta(days=90):
            return JsonResponse({
                'success': False,
                'error': 'Cannot book appointments more than 90 days in advance'
            }, status=400)
        
        # Check working hours and holidays
        if not is_working_hours(appointment_date, appointment_time):
            return JsonResponse({
                'success': False,
                'error': 'Selected time is outside working hours'
            }, status=400)
        
        if is_holiday(appointment_date):
            return JsonResponse({
                'success': False,
                'error': 'Selected date is a holiday and we are closed'
            }, status=400)
        
        # Check for conflicting appointments
        conflicting_appointments = Appointment.objects.filter(
            date=appointment_date,
            time=appointment_time,
            status__in=['pending', 'confirmed']
        )
        
        if conflicting_appointments.exists():
            return JsonResponse({
                'success': False,
                'error': 'This time slot is already booked. Please select another time.'
            }, status=400)
        
        # Create appointment
        appointment = Appointment.objects.create(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            service=service,
            date=appointment_date,
            time=appointment_time,
            duration=service.duration,
            notes=data.get('notes', ''),
            status='pending'
        )
        
        logger.info(f"Appointment created: {appointment.id} for {appointment.name}")
        
        # Send pending appointment email
        try:
            logger.info(f"Attempting to send pending appointment email to {appointment.email}")
            email_sent = send_pending_appointment_email(appointment)
            if email_sent:
                logger.info(f"Pending appointment email sent successfully to {appointment.email}")
            else:
                logger.error(f"Failed to send pending appointment email to {appointment.email}")
        except Exception as e:
            logger.error(f"Exception while sending pending appointment email: {e}")
            logger.exception("Full traceback:")
        
        # Send pending notification to customer
        try:
            from .webhook_views import send_appointment_notification
            send_appointment_notification(appointment, "pending")
        except Exception as e:
            logger.error(f"Failed to send pending notification: {e}")
        
        # Send approval request to barber
        try:
            from .webhook_views import send_approval_request_to_barber
            send_approval_request_to_barber(appointment)
        except Exception as e:
            logger.error(f"Failed to send approval request to barber: {e}")
        
        return JsonResponse({
            'success': True,
            'appointment_id': appointment.appointment_id,
            'message': 'Appointment request submitted successfully! The barber will review and confirm your appointment. You will receive a WhatsApp notification once approved.'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request format'
        }, status=400)
    except Exception as e:
        logger.error(f"Error handling booking submission: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while booking your appointment. Please try again.'
        }, status=500)

def appointment_status(request, appointment_id):
    """Check appointment status"""
    try:
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
        
        context = {
            'appointment': appointment,
            'page_title': f'Appointment Status - {appointment.appointment_id}'
        }
        return render(request, 'booking/appointment_status.html', context)
        
    except Exception as e:
        logger.error(f"Error in appointment_status view: {e}")
        messages.error(request, "Sorry, there was an error loading the appointment status.")
        return render(request, 'booking/error.html', {'error': str(e)})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Admin dashboard for managing appointments"""
    try:
        # Check if user is authenticated and is staff
        if not request.user.is_authenticated:
            return redirect('booking:admin_login')
        
        if not request.user.is_staff:
            messages.error(request, 'Access denied. Staff privileges required.')
            return redirect('booking:admin_login')
        
        # Get filter parameters
        status_filter = request.GET.get('status', '')
        date_filter = request.GET.get('date', '')
        service_filter = request.GET.get('service', '')
        
        # Build optimized query with select_related to avoid N+1 queries
        appointments = Appointment.objects.select_related('service').all()
        
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        
        if date_filter:
            appointments = appointments.filter(date=date_filter)
        
        if service_filter:
            appointments = appointments.filter(service_id=service_filter)
        
        # Order by ID (newest first)
        appointments = appointments.order_by('-id')
        
        # Pagination with larger page size for better performance
        paginator = Paginator(appointments, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Optimize statistics queries with single database hits
        from django.db.models import Count, Q
        stats = Appointment.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            confirmed=Count('id', filter=Q(status='confirmed')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            today=Count('id', filter=Q(date=timezone.now().date()))
        )
        
        # Get services for filter (cached)
        services = Service.objects.filter(is_active=True).only('id', 'name')
        
        context = {
            'page_obj': page_obj,
            'total_appointments': stats['total'],
            'pending_appointments': stats['pending'],
            'confirmed_appointments': stats['confirmed'],
            'cancelled_appointments': stats['cancelled'],
            'today_appointments': stats['today'],
            'services': services,
            'status_filter': status_filter,
            'date_filter': date_filter,
            'service_filter': service_filter,
            'page_title': 'Admin Dashboard - FitBlendz Pro'
        }
        
        return render(request, 'booking/admin_dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Error in admin_dashboard view: {e}")
        messages.error(request, "Sorry, there was an error loading the dashboard.")
        return render(request, 'booking/error.html', {'error': str(e)})

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def update_appointment_status(request, appointment_id):
    """Update appointment status via AJAX"""
    try:
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
        
        # Handle both JSON and form data
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                new_status = data.get('status')
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON data'
                }, status=400)
        else:
            new_status = request.POST.get('status')
        
        if not new_status:
            return JsonResponse({
                'success': False,
                'error': 'Status parameter is required'
            }, status=400)
        
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return JsonResponse({
                'success': False,
                'error': f'Invalid status: {new_status}. Valid options are: {", ".join([choice[0] for choice in Appointment.STATUS_CHOICES])}'
            }, status=400)
        
        old_status = appointment.status
        appointment.status = new_status
        
        # Update timestamps based on status
        if new_status == 'confirmed' and old_status != 'confirmed':
            appointment.confirmed_at = timezone.now()
        elif new_status == 'completed' and old_status != 'completed':
            appointment.completed_at = timezone.now()
        
        appointment.save()
        
        logger.info(f"Appointment {appointment_id} status updated from {old_status} to {new_status}")
        
        # Send notifications if status changed
        if old_status != new_status:
            try:
                # Send WhatsApp notification
                if new_status == 'confirmed':
                    send_appointment_notification(appointment, "confirmation")
                elif new_status == 'cancelled':
                    send_appointment_notification(appointment, "cancellation")
                elif new_status == 'completed':
                    send_appointment_notification(appointment, "update")
            except Exception as e:
                logger.error(f"Failed to send WhatsApp notification: {e}")
            
            # Send email notification
            try:
                if new_status == 'confirmed':
                    email_sent = send_status_confirmation_email(appointment)
                    if email_sent:
                        logger.info(f"Status confirmation email sent successfully to {appointment.email}")
                    else:
                        logger.warning(f"Failed to send status confirmation email to {appointment.email}")
                elif new_status == 'cancelled':
                    email_sent = send_status_cancellation_email(appointment)
                    if email_sent:
                        logger.info(f"Status cancellation email sent successfully to {appointment.email}")
                    else:
                        logger.warning(f"Failed to send status cancellation email to {appointment.email}")
                elif new_status == 'completed':
                    email_sent = send_status_completion_email(appointment)
                    if email_sent:
                        logger.info(f"Status completion email sent successfully to {appointment.email}")
                    else:
                        logger.warning(f"Failed to send status completion email to {appointment.email}")
            except Exception as e:
                logger.error(f"Failed to send status update email: {e}")
        
        return JsonResponse({
            'success': True,
            'message': f'Appointment status updated to {appointment.get_status_display()}',
            'new_status': new_status,
            'new_status_display': appointment.get_status_display()
        })
        
    except Exception as e:
        logger.error(f"Error updating appointment status: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while updating the appointment status.'
        }, status=500)

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(["POST"])
def delete_appointment(request, appointment_id):
    """Delete appointment via AJAX"""
    try:
        appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
        
        # Allow deletion of any appointment status
        appointment.delete()
        logger.info(f"Appointment {appointment_id} deleted")
        
        return JsonResponse({
            'success': True,
            'message': 'Appointment deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting appointment: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while deleting the appointment.'
        }, status=500)

def get_available_times(request):
    """Get available time slots for a given date"""
    try:
        date_str = request.GET.get('date')
        if not date_str:
            return JsonResponse({'error': 'Date parameter is required'}, status=400)
        
        appointment_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if it's a holiday
        if is_holiday(appointment_date):
            return JsonResponse({'available_times': [], 'message': 'Closed on this date'})
        
        # Get working hours for this day
        working_hours = WorkingHours.objects.filter(day=appointment_date.weekday()).first()
        
        if not working_hours or not working_hours.is_open:
            return JsonResponse({'available_times': [], 'message': 'Closed on this day'})
        
        # Generate time slots
        available_times = generate_time_slots(working_hours, appointment_date)
        
        return JsonResponse({
            'available_times': available_times,
            'working_hours': {
                'open': working_hours.open_time.strftime('%H:%M') if working_hours.open_time else None,
                'close': working_hours.close_time.strftime('%H:%M') if working_hours.close_time else None
            }
        })
        
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    except Exception as e:
        logger.error(f"Error getting available times: {e}")
        return JsonResponse({'error': 'An error occurred'}, status=500)

def generate_time_slots(working_hours, date):
    """Generate available time slots for a given date"""
    if not working_hours.open_time or not working_hours.close_time:
        return []
    
    # Get existing appointments for this date
    existing_appointments = Appointment.objects.filter(
        date=date,
        status__in=['pending', 'confirmed']
    ).values_list('time', 'duration')
    
    # Generate time slots (30-minute intervals)
    slots = []
    current_time = working_hours.open_time
    
    while current_time < working_hours.close_time:
        # Check if this slot conflicts with existing appointments
        slot_end = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()
        
        # Check for conflicts
        conflict = False
        for appt_time, appt_duration in existing_appointments:
            appt_end = (datetime.combine(date, appt_time) + timedelta(minutes=appt_duration)).time()
            
            # Check if slots overlap
            if (current_time < appt_end and slot_end > appt_time):
                conflict = True
                break
        
        if not conflict:
            slots.append(current_time.strftime('%H:%M'))
        
        # Move to next slot
        current_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()
    
    return slots

def get_working_hours(request):
    """Get working hours for all days"""
    try:
        working_hours = WorkingHours.objects.all().order_by('day')
        hours_data = {}
        
        for wh in working_hours:
            hours_data[wh.day] = {
                'is_open': wh.is_open,
                'open_time': wh.open_time.strftime('%H:%M') if wh.open_time else None,
                'close_time': wh.close_time.strftime('%H:%M') if wh.close_time else None,
                'break_start': wh.break_start.strftime('%H:%M') if wh.break_start else None,
                'break_end': wh.break_end.strftime('%H:%M') if wh.break_end else None,
                'day_name': wh.get_day_display()
            }
        
        return JsonResponse({
            'success': True,
            'working_hours': hours_data
        })
        
    except Exception as e:
        logger.error(f"Error getting working hours: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching working hours.'
        }, status=500)

def error_page(request):
    """Generic error page"""
    return render(request, 'booking/error.html', {
        'error': 'An unexpected error occurred. Please try again.',
        'page_title': 'Error - FitBlendz Pro'
    })
