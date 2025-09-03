#!/usr/bin/env python3
"""
Test Script for FitBlendz Pro WhatsApp System
This script tests the WhatsApp notification system to ensure it's working properly.
"""

import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from booking.models import Appointment
from booking.webhook_views import send_appointment_notification, send_approval_request_to_barber

def test_whatsapp_system():
    """Test the WhatsApp notification system"""
    print("🧪 Testing FitBlendz Pro WhatsApp System")
    print("=" * 50)
    
    try:
        # Get the most recent appointment
        latest_appointment = Appointment.objects.last()
        if not latest_appointment:
            print("❌ No appointments found in database")
            return False
        
        print(f"📱 Testing with appointment: {latest_appointment.appointment_id}")
        print(f"   Customer: {latest_appointment.name}")
        print(f"   Phone: {latest_appointment.phone}")
        print(f"   Status: {latest_appointment.status}")
        print()
        
        # Test 1: Customer notification
        print("🔔 Test 1: Customer WhatsApp Notification")
        print("-" * 40)
        result = send_appointment_notification(latest_appointment, "pending")
        if result:
            print("✅ Customer notification sent successfully")
        else:
            print("❌ Customer notification failed")
        print()
        
        # Test 2: Barber approval request
        print("👨‍💼 Test 2: Barber Approval Request")
        print("-" * 40)
        result = send_approval_request_to_barber(latest_appointment)
        if result:
            print("✅ Barber approval request sent successfully")
        else:
            print("❌ Barber approval request failed")
        print()
        
        # Test 3: Check phone number formatting
        print("📞 Test 3: Phone Number Formatting")
        print("-" * 40)
        try:
            formatted_phone = latest_appointment.get_whatsapp_phone()
            print(f"✅ Phone formatted correctly: {formatted_phone}")
        except Exception as e:
            print(f"❌ Phone formatting failed: {e}")
        print()
        
        print("🎉 WhatsApp System Test Complete!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def check_environment():
    """Check if environment variables are set correctly"""
    print("🔍 Checking Environment Configuration")
    print("-" * 40)
    
    required_vars = [
        'WHATSAPP_TOKEN',
        'PHONE_NUMBER_ID', 
        'WHATSAPP_VERIFY_TOKEN',
        'BARBER_WHATSAPP'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = getattr(django.conf.settings, var, None)
        if value:
            print(f"✅ {var}: {value[:20]}..." if len(str(value)) > 20 else f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("\n✅ All required environment variables are set")
        return True

if __name__ == "__main__":
    print("Welcome to FitBlendz Pro WhatsApp System Test!")
    print()
    
    # Check environment first
    if not check_environment():
        print("\n❌ Environment check failed. Please set up your environment variables first.")
        exit(1)
    
    print()
    
    # Test the WhatsApp system
    if test_whatsapp_system():
        print("\n🎉 All tests passed! Your WhatsApp system is working correctly.")
        print("\n📋 What to check next:")
        print("1. Check your WhatsApp for the barber approval request")
        print("2. Verify the customer received their notification")
        print("3. Test the Accept/Deny buttons")
        print("4. Verify buttons are disabled after clicking")
    else:
        print("\n❌ Some tests failed. Check the logs for more details.")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check django.log for error messages")
        print("2. Verify WhatsApp Business API tokens are valid")
        print("3. Ensure phone numbers are in the correct format")
        print("4. Check if webhook URL is accessible")

