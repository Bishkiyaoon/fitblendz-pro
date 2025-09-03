#!/usr/bin/env python3
"""
Gmail SMTP Setup Script for FitBlendz Pro
This script helps you set up Gmail SMTP for permanent email functionality.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with Gmail SMTP configuration"""
    env_content = """# Email Configuration (Gmail SMTP - PERMANENT SOLUTION)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=bjot404@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=bjot404@gmail.com

# WhatsApp Configuration
WHATSAPP_TOKEN=EAALYGYkTohABPFTc7s3aS2VNY6VCWLr7QoLFRBFRfnsZBPEJ3JWvEMxlyZAb7LW42itPLgPtcw8qBBlv0HaHqOmoR2K3PlPZBYkMZCxRNJRAFOVVPCYytVLNTJvW6zj714XQ6ZAw427pI7s7YOw3qZArbl9Pvi6nOFwlBLKKUN9FNCogEZC7duZCYFVZAPdit3phPtgZDZD
PHONE_NUMBER_ID=720494921152084
WHATSAPP_VERIFY_TOKEN=fitblendz_whatsapp_verify_7c2f4b1e
BARBER_WHATSAPP=+916239514954

# Django Settings
DEBUG=True
DJANGO_SECRET_KEY=django-insecure-improved-secret-key-2024
ALLOWED_HOSTS=localhost,127.0.0.1,2557bbf4925b.ngrok-free.app
"""
    
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        os.rename('.env', '.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("\n📝 IMPORTANT: You need to update the EMAIL_HOST_PASSWORD in .env file")
    print("   Replace 'your-16-char-app-password' with your actual Gmail App Password")

def print_setup_instructions():
    """Print step-by-step setup instructions"""
    print("\n" + "="*60)
    print("🔧 GMAIL SMTP SETUP INSTRUCTIONS")
    print("="*60)
    
    print("\n📱 Step 1: Enable 2-Factor Authentication on Gmail")
    print("   1. Go to https://myaccount.google.com/")
    print("   2. Click Security → 2-Step Verification")
    print("   3. Enable 2-Step Verification if not already enabled")
    
    print("\n🔑 Step 2: Generate App Password")
    print("   1. Go to https://myaccount.google.com/")
    print("   2. Click Security → App passwords")
    print("   3. Select 'Mail' and 'Other (Custom name)'")
    print("   4. Enter name: 'FitBlendz Pro'")
    print("   5. Click Generate")
    print("   6. Copy the 16-character password (e.g., 'abcd efgh ijkl mnop')")
    
    print("\n📝 Step 3: Update .env file")
    print("   1. Open the .env file in your project")
    print("   2. Replace 'your-16-char-app-password' with your actual app password")
    print("   3. Save the file")
    
    print("\n🧪 Step 4: Test Email Configuration")
    print("   Run: python manage.py shell -c \"from django.core.mail import send_mail; from django.conf import settings; send_mail('Test', 'Test email', settings.DEFAULT_FROM_EMAIL, ['your-email@gmail.com'])\"")
    
    print("\n" + "="*60)

def test_email_config():
    """Test the current email configuration"""
    print("\n🧪 Testing current email configuration...")
    
    try:
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
        import django
        django.setup()
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        print(f"📧 Email Host: {settings.EMAIL_HOST}")
        print(f"📧 Email Port: {settings.EMAIL_PORT}")
        print(f"📧 Email User: {settings.EMAIL_HOST_USER}")
        print(f"📧 Use TLS: {settings.EMAIL_USE_TLS}")
        print(f"📧 Use SSL: {settings.EMAIL_USE_SSL}")
        
        # Test email sending
        test_email = input("\n📧 Enter your email address to test: ").strip()
        
        if test_email:
            print("📤 Sending test email...")
            send_mail(
                'Test Email - FitBlendz Pro',
                'This is a test email to verify SMTP configuration is working correctly.',
                settings.DEFAULT_FROM_EMAIL,
                [test_email],
                fail_silently=False,
            )
            print("✅ Test email sent successfully!")
            print("📧 Check your inbox (and spam folder)")
        else:
            print("⚠️  No email address provided. Skipping test.")
            
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("\n💡 This is expected if you haven't set up the Gmail App Password yet.")
        print("   Follow the setup instructions above first.")

def main():
    """Main setup function"""
    print("🚀 FitBlendz Pro - Gmail SMTP Setup")
    print("="*50)
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Create .env file with Gmail configuration")
        print("2. Show setup instructions")
        print("3. Test current email configuration")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            print_setup_instructions()
        elif choice == '3':
            test_email_config()
        elif choice == '4':
            print("👋 Setup complete! Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()

