from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid

class Service(models.Model):
    """Barber services available for booking"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Appointment(models.Model):
    """Appointment booking model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    # Unique identifier
    appointment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Customer information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    
    # Appointment details
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    
    # Status and notes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, help_text="Special requests or notes")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # WhatsApp integration
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['date', 'time']),
            models.Index(fields=['status']),
            models.Index(fields=['phone']),
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['appointment_id']),
            models.Index(fields=['status', 'date']),  # Composite index for common queries
            models.Index(fields=['service', 'date']),  # For service-based queries
        ]

    def __str__(self):
        return f"{self.name} - {self.service.name} on {self.date} at {self.time}"

    def get_status_display_class(self):
        """Return CSS class for status display"""
        status_classes = {
            'pending': 'status-pending',
            'confirmed': 'status-confirmed',
            'completed': 'status-completed',
            'cancelled': 'status-cancelled',
            'no_show': 'status-no-show',
        }
        return status_classes.get(self.status, 'status-default')

    def is_past_appointment(self):
        """Check if appointment is in the past"""
        now = timezone.now()
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time)
        )
        return appointment_datetime < now

    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        return self.status in ['pending', 'confirmed'] and not self.is_past_appointment()

    def get_duration_display(self):
        """Return formatted duration"""
        hours = self.duration // 60
        minutes = self.duration % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
        return f"{minutes}m"

    def get_whatsapp_phone(self):
        """Return phone number formatted for WhatsApp API"""
        # Remove any non-digit characters except +
        phone = str(self.phone).strip()
        # Ensure it starts with country code
        if not phone.startswith('+'):
            # Assume US number if no country code
            if len(phone) == 10:
                phone = '+1' + phone
            elif len(phone) == 11 and phone.startswith('1'):
                phone = '+' + phone
            else:
                phone = '+1' + phone
        return phone

class WorkingHours(models.Model):
    """Barber shop working hours"""
    DAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]
    
    day = models.IntegerField(choices=DAY_CHOICES, unique=True)
    is_open = models.BooleanField(default=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)
    break_start = models.TimeField(null=True, blank=True)
    break_end = models.TimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['day']
        verbose_name_plural = 'Working Hours'

    def __str__(self):
        if not self.is_open:
            return f"{self.get_day_display()} - Closed"
        return f"{self.get_day_display()} - {self.open_time} to {self.close_time}"

class Holiday(models.Model):
    """Holiday dates when shop is closed"""
    date = models.DateField(unique=True)
    description = models.CharField(max_length=200)
    is_recurring = models.BooleanField(default=False, help_text="Recurring holiday (e.g., Christmas)")
    
    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.description}"

    def is_this_year(self):
        """Check if holiday is in current year"""
        return self.date.year == timezone.now().year
