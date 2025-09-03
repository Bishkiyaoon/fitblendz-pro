from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Service, Appointment, WorkingHours, Holiday

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Service Information', {
            'fields': ('name', 'description', 'price', 'duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'appointment_id_short', 'customer_name', 'service', 'date', 'time', 
        'status', 'phone', 'created_at'
    ]
    list_filter = [
        'status', 'date', 'service', 'created_at', 'whatsapp_sent'
    ]
    search_fields = ['name', 'email', 'phone', 'appointment_id']
    ordering = ['-date', '-time']
    readonly_fields = [
        'appointment_id', 'created_at', 'updated_at', 'confirmed_at', 
        'completed_at', 'whatsapp_sent_at'
    ]
    date_hierarchy = 'date'
    list_per_page = 25  # Pagination for better performance
    list_max_show_all = 100  # Limit bulk operations
    
    def get_queryset(self, request):
        """Optimize queries with select_related to avoid N+1 queries"""
        return super().get_queryset(request).select_related('service')
    
    fieldsets = (
        ('Appointment Information', {
            'fields': ('appointment_id', 'service', 'date', 'time', 'duration', 'status')
        }),
        ('Customer Details', {
            'fields': ('name', 'email', 'phone', 'notes')
        }),
        ('WhatsApp Integration', {
            'fields': ('whatsapp_sent', 'whatsapp_sent_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['confirm_appointments', 'mark_completed', 'send_whatsapp_reminders']
    
    def appointment_id_short(self, obj):
        """Display shortened appointment ID"""
        return str(obj.appointment_id)[:8] + "..."
    appointment_id_short.short_description = "Appointment ID"
    
    def customer_name(self, obj):
        """Display customer name with link to details"""
        return obj.name
    customer_name.short_description = "Customer"
    
    def confirm_appointments(self, request, queryset):
        """Action to confirm selected appointments"""
        from django.utils import timezone
        updated = queryset.update(
            status='confirmed', 
            confirmed_at=timezone.now()
        )
        self.message_user(
            request, 
            f"Successfully confirmed {updated} appointment(s)."
        )
    confirm_appointments.short_description = "Confirm selected appointments"
    
    def mark_completed(self, request, queryset):
        """Action to mark appointments as completed"""
        from django.utils import timezone
        updated = queryset.update(
            status='completed', 
            completed_at=timezone.now()
        )
        self.message_user(
            request, 
            f"Successfully marked {updated} appointment(s) as completed."
        )
    mark_completed.short_description = "Mark selected appointments as completed"
    
    def send_whatsapp_reminders(self, request, queryset):
        """Action to send WhatsApp reminders"""
        # This would integrate with your WhatsApp service
        self.message_user(
            request, 
            f"WhatsApp reminders would be sent for {queryset.count()} appointment(s)."
        )
    send_whatsapp_reminders.short_description = "Send WhatsApp reminders"

@admin.register(WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ['day', 'is_open', 'open_time', 'close_time', 'break_display']
    list_filter = ['is_open']
    ordering = ['day']
    
    def break_display(self, obj):
        """Display break time information"""
        if obj.break_start and obj.break_end:
            return f"{obj.break_start} - {obj.break_end}"
        return "No break"
    break_display.short_description = "Break Time"
    
    fieldsets = (
        ('Day Settings', {
            'fields': ('day', 'is_open')
        }),
        ('Working Hours', {
            'fields': ('open_time', 'close_time'),
            'classes': ('collapse',)
        }),
        ('Break Time', {
            'fields': ('break_start', 'break_end'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ['date', 'description', 'is_recurring', 'is_this_year']
    list_filter = ['is_recurring', 'date']
    search_fields = ['description']
    ordering = ['date']
    
    def is_this_year(self, obj):
        """Check if holiday is in current year"""
        return obj.is_this_year()
    is_this_year.boolean = True
    is_this_year.short_description = "This Year"

# Customize admin site
admin.site.site_header = "FitBlendz Pro - Admin Dashboard"
admin.site.site_title = "FitBlendz Pro Admin"
admin.site.index_title = "Welcome to FitBlendz Pro Administration"
