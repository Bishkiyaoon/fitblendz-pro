from django.urls import path
from . import views
from . import webhook_views

app_name = 'booking'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('book/', views.booking_page, name='booking_page'),
    path('status/<uuid:appointment_id>/', views.appointment_status, name='appointment_status'),
    
    # Admin pages
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    
    # API endpoints
    path('api/delete-appointment/<uuid:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('api/update-appointment-status/<uuid:appointment_id>/', views.update_appointment_status, name='update_appointment_status'),
    path('api/available-times/', views.get_available_times, name='get_available_times'),
    
    # WhatsApp webhook
    path('webhook/', webhook_views.whatsapp_webhook, name='whatsapp_webhook'),
    path('whatsapp-webhook/', webhook_views.whatsapp_webhook, name='whatsapp_webhook_alt'),
    
    # Error page
    path('error/', views.error_page, name='error_page'),
]
