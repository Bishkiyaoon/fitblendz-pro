from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils import timezone
import json
import logging
import requests
from .models import Appointment

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    """WhatsApp webhook handler for both verification and incoming messages"""
    logger.info(f"Webhook request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR', 'unknown')}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request GET params: {dict(request.GET)}")
    """
    Improved WhatsApp webhook handler that addresses all common issues:
    1. CSRF exempt
    2. Clean response format
    3. Proper logging
    4. No extra content in verification response
    5. Better error handling
    """
    
    if request.method == "GET":
        # WhatsApp verification
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        logger.info(f"Webhook verification request: mode={mode}, token={token}, challenge={challenge}")
        
        # Check if all required parameters are present
        if not all([mode, token, challenge]):
            logger.warning(f"Missing required parameters: mode={mode}, token={token}, challenge={challenge}")
            # Return a more helpful error message for debugging
            return HttpResponse(
                'Bad Request: Missing required WhatsApp verification parameters. '
                'Expected: hub.mode, hub.verify_token, hub.challenge', 
                status=400, 
                content_type='text/plain'
            )
        
        # Verify the token
        if mode == 'subscribe' and token == settings.WHATSAPP_VERIFY_TOKEN:
            logger.info(f"Verification successful for token: {token}")
            # Return ONLY the challenge string - this is critical!
            return HttpResponse(challenge, content_type='text/plain')
        else:
            logger.warning(f"Verification failed: mode={mode}, token={token}, expected={settings.WHATSAPP_VERIFY_TOKEN}")
            return HttpResponse('Forbidden', status=403, content_type='text/plain')
    
    elif request.method == "POST":
        try:
            # Parse incoming webhook data
            data = json.loads(request.body)
            logger.info(f"Received webhook POST data: {json.dumps(data, indent=2)}")
            
            # Process the webhook data
            if 'entry' in data and len(data['entry']) > 0:
                entry = data['entry'][0]
                if 'changes' in entry and len(entry['changes']) > 0:
                    change = entry['changes'][0]
                    if 'value' in change and 'messages' in change['value']:
                        messages = change['value']['messages']
                        for message in messages:
                            logger.info(f"Processing message: {message}")
                            handle_whatsapp_message(message)
            
            # Return simple OK response
            return HttpResponse('OK', content_type='text/plain')
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in webhook: {e}")
            return HttpResponse('Invalid JSON', status=400, content_type='text/plain')
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return HttpResponse('Internal Error', status=500, content_type='text/plain')
    
    # This should never be reached due to @require_http_methods
    return HttpResponse('Method Not Allowed', status=405, content_type='text/plain')

def handle_whatsapp_message(message):
    """Handle incoming WhatsApp message with improved logic"""
    try:
        # Extract message details
        from_number = message.get('from')
        message_type = message.get('type')
        timestamp = message.get('timestamp')
        
        logger.info(f"Processing {message_type} message from {from_number}")
        
        if message_type == 'text':
            text = message.get('text', {}).get('body', '').lower()
            logger.info(f"Text message: {text}")
            
            # Handle different types of text messages
            if 'cancel' in text or 'cancelar' in text:
                handle_cancellation_request(from_number, text)
            elif 'confirm' in text or 'confirmar' in text:
                handle_confirmation_request(from_number, text)
            elif 'status' in text or 'estado' in text:
                handle_status_request(from_number, text)
            elif 'help' in text or 'ayuda' in text:
                send_help_message(from_number)
            elif 'approve' in text or 'approve' in text:
                handle_approval_request(from_number, text)
            elif 'deny' in text or 'reject' in text:
                handle_rejection_request(from_number, text)
            elif 'pending' in text or 'list' in text:
                handle_pending_appointments_request(from_number, text)
            else:
                send_default_response(from_number)
        
        elif message_type == 'interactive':
            # Handle button responses
            interactive = message.get('interactive', {})
            if interactive.get('type') == 'button_reply':
                button_id = interactive.get('button_reply', {}).get('id', '')
                logger.info(f"Button response: {button_id}")
                
                if button_id.startswith('approve_'):
                    appointment_id = button_id.replace('approve_', '')
                    handle_button_approval(from_number, appointment_id)
                elif button_id.startswith('deny_'):
                    appointment_id = button_id.replace('deny_', '')
                    handle_button_rejection(from_number, appointment_id)
                else:
                    logger.warning(f"Unknown button ID: {button_id}")
                
    except Exception as e:
        logger.error(f"Error handling WhatsApp message: {e}")

def handle_cancellation_request(phone_number, message_text):
    """Handle appointment cancellation requests"""
    try:
        # Extract appointment ID from message if present
        # This is a simplified version - you can enhance it
        logger.info(f"Handling cancellation request from {phone_number}")
        
        # Send cancellation confirmation
        response_text = "To cancel your appointment, please contact us directly or use the cancellation link in your confirmation email."
        send_whatsapp_message(phone_number, response_text)
        
    except Exception as e:
        logger.error(f"Error handling cancellation request: {e}")

def handle_confirmation_request(phone_number, message_text):
    """Handle appointment confirmation requests"""
    try:
        logger.info(f"Handling confirmation request from {phone_number}")
        
        response_text = "To confirm your appointment, please check your email for the confirmation link or contact us directly."
        send_whatsapp_message(phone_number, response_text)
        
    except Exception as e:
        logger.error(f"Error handling confirmation request: {e}")

def handle_status_request(phone_number, message_text):
    """Handle appointment status requests"""
    try:
        logger.info(f"Handling status request from {phone_number}")
        
        # Find appointments for this phone number
        appointments = Appointment.objects.filter(phone=phone_number).order_by('-date', '-time')
        
        if appointments.exists():
            latest = appointments.first()
            status_text = f"Your latest appointment: {latest.service.name} on {latest.date} at {latest.time} - Status: {latest.get_status_display()}"
        else:
            status_text = "No appointments found for this phone number. Please check your booking details."
        
        send_whatsapp_message(phone_number, status_text)
        
    except Exception as e:
        logger.error(f"Error handling status request: {e}")

def send_help_message(phone_number):
    """Send help message with available commands"""
    # Check if this is the barber's number (normalize both numbers)
    barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
    incoming_number = str(phone_number).replace('+', '').replace(' ', '')
    
    if incoming_number == barber_number:
        help_text = """Barber Commands:
• 'approve' - Approve pending appointment
• 'deny' - Reject pending appointment
• 'pending' - List all pending appointments
• 'status' - Check appointment status
• 'help' - Show this help message

For immediate assistance, please contact us directly."""
    else:
        help_text = """Customer Commands:
• 'status' - Check appointment status
• 'cancel' - Cancel appointment
• 'confirm' - Confirm appointment
• 'help' - Show this help message

For immediate assistance, please contact us directly."""
    
    send_whatsapp_message(phone_number, help_text)

def send_default_response(phone_number):
    """Send default response for unrecognized messages"""
    default_text = "Thank you for your message. Type 'help' to see available commands or contact us directly for assistance."
    send_whatsapp_message(phone_number, default_text)

def handle_approval_request(phone_number, message_text):
    """Handle appointment approval requests from barber"""
    try:
        logger.info(f"Handling approval request from barber: {phone_number}")
        
        # Check if this is the barber's number (normalize both numbers)
        barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
        incoming_number = str(phone_number).replace('+', '').replace(' ', '')
        
        logger.info(f"Checking authorization: incoming={incoming_number}, barber={barber_number}")
        
        if incoming_number == barber_number:
            # Find pending appointments
            pending_appointments = Appointment.objects.filter(status='pending').order_by('date', 'time')
            
            if pending_appointments.exists():
                # Get the oldest pending appointment
                appointment = pending_appointments.first()
                
                # Update appointment status to confirmed
                appointment.status = 'confirmed'
                appointment.confirmed_at = timezone.now()
                appointment.save()
                
                # Send confirmation to customer
                send_appointment_notification(appointment, "confirmation")
                
                # Send confirmation email to customer
                try:
                    from .utils import send_status_confirmation_email
                    email_sent = send_status_confirmation_email(appointment)
                    if email_sent:
                        logger.info(f"Confirmation email sent successfully to {appointment.email}")
                    else:
                        logger.warning(f"Failed to send confirmation email to {appointment.email}")
                except Exception as e:
                    logger.error(f"Failed to send confirmation email: {e}")
                
                # Send confirmation to barber
                barber_message = f"Appointment approved!\n\nCustomer: {appointment.name}\nService: {appointment.service.name}\nDate: {appointment.date}\nTime: {appointment.time.strftime('%I:%M %p')}\n\nCustomer has been notified."
                send_whatsapp_message(phone_number, barber_message)
                
                logger.info(f"Appointment {appointment.id} approved by barber")
            else:
                send_whatsapp_message(phone_number, "No pending appointments to approve.")
        else:
            send_whatsapp_message(phone_number, "You are not authorized to approve appointments.")
            
    except Exception as e:
        logger.error(f"Error handling approval request: {e}")

def handle_rejection_request(phone_number, message_text):
    """Handle appointment rejection requests from barber"""
    try:
        logger.info(f"Handling rejection request from barber: {phone_number}")
        
        # Check if this is the barber's number (normalize both numbers)
        barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
        incoming_number = str(phone_number).replace('+', '').replace(' ', '')
        
        if incoming_number == barber_number:
            # Find pending appointments
            pending_appointments = Appointment.objects.filter(status='pending').order_by('date', 'time')
            
            if pending_appointments.exists():
                # Get the oldest pending appointment
                appointment = pending_appointments.first()
                
                # Update appointment status to cancelled
                appointment.status = 'cancelled'
                appointment.save()
                
                # Send cancellation to customer
                send_appointment_notification(appointment, "cancellation")
                
                # Send cancellation email to customer
                try:
                    from .utils import send_status_cancellation_email
                    email_sent = send_status_cancellation_email(appointment)
                    if email_sent:
                        logger.info(f"Cancellation email sent successfully to {appointment.email}")
                    else:
                        logger.warning(f"Failed to send cancellation email to {appointment.email}")
                except Exception as e:
                    logger.error(f"Failed to send cancellation email: {e}")
                
                # Send confirmation to barber
                barber_message = f"Appointment rejected!\n\nCustomer: {appointment.name}\nService: {appointment.service.name}\nDate: {appointment.date}\nTime: {appointment.time.strftime('%I:%M %p')}\n\nCustomer has been notified."
                send_whatsapp_message(phone_number, barber_message)
                
                logger.info(f"Appointment {appointment.id} rejected by barber")
            else:
                send_whatsapp_message(phone_number, "No pending appointments to reject.")
        else:
            send_whatsapp_message(phone_number, "You are not authorized to reject appointments.")
            
    except Exception as e:
        logger.error(f"Error handling rejection request: {e}")

def handle_button_approval(phone_number, appointment_id):
    """Handle button approval for specific appointment"""
    try:
        logger.info(f"Handling button approval from barber: {phone_number} for appointment: {appointment_id}")
        
        # Check if this is the barber's number (normalize both numbers)
        barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
        incoming_number = str(phone_number).replace('+', '').replace(' ', '')
        
        if incoming_number == barber_number:
            # Find the specific appointment
            try:
                appointment = Appointment.objects.get(appointment_id=appointment_id, status='pending')
            except Appointment.DoesNotExist:
                send_whatsapp_message(phone_number, f"Appointment {appointment_id} not found or already processed.")
                return
            
            # Update appointment status to confirmed
            appointment.status = 'confirmed'
            appointment.confirmed_at = timezone.now()
            appointment.save()
            
            # Send confirmation to customer
            send_appointment_notification(appointment, "confirmation")
            
            # Send confirmation email to customer
            try:
                from .utils import send_status_confirmation_email
                email_sent = send_status_confirmation_email(appointment)
                if email_sent:
                    logger.info(f"Confirmation email sent successfully to {appointment.email}")
                else:
                    logger.warning(f"Failed to send confirmation email to {appointment.email}")
            except Exception as e:
                logger.error(f"Failed to send confirmation email: {e}")
            
            # Send confirmation to barber
            barber_message = f"Appointment approved!\n\nCustomer: {appointment.name}\nService: {appointment.service.name}\nDate: {appointment.date}\nTime: {appointment.time.strftime('%I:%M %p')}\n\nCustomer has been notified."
            send_whatsapp_message(phone_number, barber_message)
            
            # Send button disabled message to indicate action is complete
            send_button_disabled_message(phone_number, appointment_id, "approved")
            
            logger.info(f"Appointment {appointment_id} approved by barber via button")
        else:
            send_whatsapp_message(phone_number, "You are not authorized to approve appointments.")
            
    except Exception as e:
        logger.error(f"Error handling button approval: {e}")

def handle_button_rejection(phone_number, appointment_id):
    """Handle button rejection for specific appointment"""
    try:
        logger.info(f"Handling button rejection from barber: {phone_number} for appointment: {appointment_id}")
        
        # Check if this is the barber's number (normalize both numbers)
        barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
        incoming_number = str(phone_number).replace('+', '').replace(' ', '')
        
        if incoming_number == barber_number:
            # Find the specific appointment
            try:
                appointment = Appointment.objects.get(appointment_id=appointment_id, status='pending')
            except Appointment.DoesNotExist:
                send_whatsapp_message(phone_number, f"Appointment {appointment_id} not found or already processed.")
                return
            
            # Update appointment status to cancelled
            appointment.status = 'cancelled'
            appointment.save()
            
            # Send cancellation to customer
            send_appointment_notification(appointment, "cancellation")
            
            # Send cancellation email to customer
            try:
                from .utils import send_status_cancellation_email
                email_sent = send_status_cancellation_email(appointment)
                if email_sent:
                    logger.info(f"Cancellation email sent successfully to {appointment.email}")
                else:
                    logger.warning(f"Failed to send cancellation email to {appointment.email}")
            except Exception as e:
                logger.error(f"Failed to send cancellation email: {e}")
            
            # Send confirmation to barber
            barber_message = f"Appointment rejected!\n\nCustomer: {appointment.name}\nService: {appointment.service.name}\nDate: {appointment.date}\nTime: {appointment.time.strftime('%I:%M %p')}\n\nCustomer has been notified."
            send_whatsapp_message(phone_number, barber_message)
            
            # Send button disabled message to indicate action is complete
            send_button_disabled_message(phone_number, appointment_id, "rejected")
            
            logger.info(f"Appointment {appointment_id} rejected by barber via button")
        else:
            send_whatsapp_message(phone_number, "You are not authorized to reject appointments.")
            
    except Exception as e:
        logger.error(f"Error handling button rejection: {e}")

def handle_pending_appointments_request(phone_number, message_text):
    """Handle request to list pending appointments"""
    try:
        logger.info(f"Handling pending appointments request from: {phone_number}")
        
        # Check if this is the barber's number (normalize both numbers)
        barber_number = str(settings.BARBER_WHATSAPP).replace('+', '').replace(' ', '')
        incoming_number = str(phone_number).replace('+', '').replace(' ', '')
        
        if incoming_number == barber_number:
            # Find all pending appointments
            pending_appointments = Appointment.objects.filter(status='pending').order_by('date', 'time')
            
            if pending_appointments.exists():
                message = "Pending Appointments:\n\n"
                for i, appointment in enumerate(pending_appointments, 1):
                    message += f"{i}. {appointment.name} - {appointment.service.name}\n"
                    message += f"   Date: {appointment.date} at {appointment.time}\n"
                    message += f"   Phone: {appointment.phone}\n"
                    message += f"   Email: {appointment.email}\n"
                    if appointment.notes:
                        message += f"   Notes: {appointment.notes}\n"
                    message += f"   ID: {appointment.appointment_id}\n\n"
                
                message += "To approve the oldest pending appointment, reply: APPROVE\n"
                message += "To reject the oldest pending appointment, reply: DENY"
            else:
                message = "No pending appointments at the moment."
            
            send_whatsapp_message(phone_number, message)
        else:
            send_whatsapp_message(phone_number, "You are not authorized to view pending appointments.")
            
    except Exception as e:
        logger.error(f"Error handling pending appointments request: {e}")

def send_whatsapp_message(phone_number, message_text):
    """Send WhatsApp message with improved error handling"""
    try:
        # Format phone number for WhatsApp
        if hasattr(phone_number, 'get_whatsapp_phone'):
            # If it's an Appointment object, use the method
            formatted_phone = phone_number.get_whatsapp_phone()
        else:
            # If it's a string, format it manually
            digits = ''.join(filter(str.isdigit, str(phone_number)))
            if len(digits) == 10:
                formatted_phone = f"+91{digits}"
            elif len(digits) > 10:
                formatted_phone = f"+{digits}"
            else:
                formatted_phone = phone_number
        
        logger.info(f"Sending WhatsApp message to: {formatted_phone}")
        
        # WhatsApp Business API endpoint
        url = f"https://graph.facebook.com/v20.0/{settings.PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": formatted_phone,
            "type": "text",
            "text": {"body": message_text}
        }
        
        logger.info(f"WhatsApp API Request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        logger.info(f"WhatsApp API Response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            message_id = data.get('messages', [{}])[0].get('id', 'Unknown')
            logger.info(f"WhatsApp message sent successfully to {formatted_phone} (ID: {message_id})")
            return True
        elif response.status_code == 400:
            # Check for specific error types
            try:
                error_data = response.json()
                error_code = error_data.get('error', {}).get('code')
                error_message = error_data.get('error', {}).get('message', '')
                
                if error_code == 131030:  # Recipient not in allowed list
                    logger.warning(f"WhatsApp: Phone number {formatted_phone} not in allowed list. This is normal during development. Error: {error_message}")
                    return False
                elif error_code == 100:  # Invalid parameter
                    logger.error(f"WhatsApp: Invalid parameter - {error_message}")
                    return False
                else:
                    logger.error(f"WhatsApp API error {error_code}: {error_message}")
                    return False
            except:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
        else:
            logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout sending WhatsApp message to {phone_number}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error sending WhatsApp message: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return False

def send_appointment_notification(appointment, notification_type="confirmation"):
    """Send appointment notifications via WhatsApp with fallback handling"""
    try:
        phone_number = appointment.get_whatsapp_phone()
        logger.info(f"Sending {notification_type} notification to: {phone_number}")
        
        if notification_type == "pending":
            message = f"""Appointment Request Submitted

Hi {appointment.name},

Your appointment request has been submitted successfully!

Service: {appointment.service.name}
Date: {appointment.date}
Time: {appointment.time.strftime('%I:%M %p')}
Duration: {appointment.get_duration_display()}
Status: Pending Approval

The barber will review your request and send you a confirmation shortly.

Best regards,
FitBlendz Team"""
        
        elif notification_type == "confirmation":
            message = f"""Appointment Confirmed!

Hi {appointment.name},

Your appointment for {appointment.service.name} has been confirmed for {appointment.date} at {appointment.time.strftime('%I:%M %p')}.

Duration: {appointment.get_duration_display()}
Status: Confirmed

We look forward to seeing you!

Best regards,
FitBlendz Team"""
        
        elif notification_type == "reminder":
            message = f"""Appointment Reminder!

Hi {appointment.name},

This is a friendly reminder about your appointment tomorrow:

Service: {appointment.service.name}
Date: {appointment.date}
Time: {appointment.time.strftime('%I:%M %p')}

Please arrive 10 minutes early.

See you soon!
FitBlendz Team"""
        
        elif notification_type == "cancellation":
            message = f"""Appointment Cancelled

Hi {appointment.name},

Your appointment for {appointment.service.name} on {appointment.date} at {appointment.time.strftime('%I:%M %p')} has been cancelled.

To reschedule, please visit our website or contact us directly.

We apologize for any inconvenience.

FitBlendz Team"""
        
        else:
            message = f"""Appointment Update

Hi {appointment.name},

Your appointment details:
Service: {appointment.service.name}
Date: {appointment.date}
Time: {appointment.time.strftime('%I:%M %p')}
Status: {appointment.get_status_display()}

FitBlendz Team"""
        
        # Send the message
        success = send_whatsapp_message(phone_number, message)
        
        if success:
            # Update appointment record
            appointment.whatsapp_sent = True
            appointment.whatsapp_sent_at = timezone.now()
            appointment.save()
            logger.info(f"WhatsApp notification sent successfully for appointment {appointment.id}")
        else:
            # WhatsApp failed - this is normal during development
            logger.warning(f"WhatsApp notification failed for appointment {appointment.id} - phone number may not be in allowed list")
            # Don't mark as failed since this is expected during development
            
        return success
        
    except Exception as e:
        logger.error(f"Error sending appointment notification: {e}")
        return False

def send_whatsapp_interactive_message(phone_number, message_text, appointment_id):
    """Send WhatsApp interactive message with buttons"""
    try:
        # Format phone number for WhatsApp
        if hasattr(phone_number, 'get_whatsapp_phone'):
            formatted_phone = phone_number.get_whatsapp_phone()
        else:
            digits = ''.join(filter(str.isdigit, str(phone_number)))
            if len(digits) == 10:
                formatted_phone = f"+91{digits}"
            elif len(digits) > 10:
                formatted_phone = f"+{digits}"
            else:
                formatted_phone = phone_number
        
        logger.info(f"Sending interactive WhatsApp message to: {formatted_phone}")
        
        # WhatsApp Business API endpoint
        url = f"https://graph.facebook.com/v20.0/{settings.PHONE_NUMBER_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": formatted_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": message_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": f"approve_{appointment_id}",
                                "title": "Accept"
                            }
                        },
                        {
                            "type": "reply",
                            "reply": {
                                "id": f"deny_{appointment_id}",
                                "title": "Deny"
                            }
                        }
                    ]
                }
            }
        }
        
        logger.info(f"Interactive WhatsApp API Request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        logger.info(f"Interactive WhatsApp API Response: {response.status_code} - {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            message_id = data.get('messages', [{}])[0].get('id', 'Unknown')
            logger.info(f"Interactive WhatsApp message sent successfully to {formatted_phone} (ID: {message_id})")
            return True
        elif response.status_code == 400:
            # Check for specific error types
            try:
                error_data = response.json()
                error_code = error_data.get('error', {}).get('code')
                error_message = error_data.get('error', {}).get('message', '')
                
                if error_code == 131030:  # Recipient not in allowed list
                    logger.warning(f"WhatsApp Interactive: Phone number {formatted_phone} not in allowed list. This is normal during development. Error: {error_message}")
                    return False
                else:
                    logger.error(f"WhatsApp Interactive API error {error_code}: {error_message}")
                    return False
            except:
                logger.error(f"WhatsApp Interactive API error: {response.status_code} - {response.text}")
                return False
        else:
            logger.error(f"WhatsApp Interactive API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"Timeout sending interactive WhatsApp message to {phone_number}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error sending interactive WhatsApp message: {e}")
        return False
    except Exception as e:
        logger.error(f"Error sending interactive WhatsApp message: {e}")
        return False

def send_approval_request_to_barber(appointment):
    """Send approval request to barber for new appointment with interactive buttons"""
    try:
        barber_phone = settings.BARBER_WHATSAPP
        logger.info(f"Sending approval request to barber: {barber_phone}")
        
        # Format time with AM/PM
        time_str = appointment.time.strftime('%I:%M %p')
        
        message = f"""New Appointment Request

Customer: {appointment.name}
Phone: {appointment.phone}
Email: {appointment.email}
Service: {appointment.service.name}
Date: {appointment.date}
Time: {time_str}
Duration: {appointment.get_duration_display()}
Notes: {appointment.notes or 'None'}

Appointment ID: {appointment.appointment_id}"""
        
        # Send interactive message with buttons
        success = send_whatsapp_interactive_message(barber_phone, message, appointment.appointment_id)
        
        if success:
            logger.info(f"Interactive approval request sent to barber for appointment {appointment.id}")
        else:
            logger.warning(f"Failed to send interactive approval request to barber for appointment {appointment.id} - this is normal during development")
            
        return success
        
    except Exception as e:
        logger.error(f"Error sending approval request to barber: {e}")
        return False
