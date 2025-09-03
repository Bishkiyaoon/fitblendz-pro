#!/usr/bin/env python3
"""
Setup script for FitBlendz Pro
"""
import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_project():
    """Set up the FitBlendz Pro project"""
    print("🚀 Setting up FitBlendz Pro...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# FitBlendz Pro Environment Configuration
DEBUG=True
DJANGO_SECRET_KEY=django-insecure-improved-secret-key-2024
WHATSAPP_TOKEN=EAALYGYkTohABPQ97AghaFnDLR3DkbHFsz6foZAKZCcI3P5OHV9MR6Pu34In3eKxi47sqewSzkzGGFPBgXud6sz8gg7Iw2GMYTOsDY9NeVKZCyfVswBtYDhlQyZBIBVPPokJZBhCGtEwFDtRAThXZAaAZCN8XorKbRykZAipfunZB5dSaInbHzjVboHoNyedXPMuHSiVfcmLGWmiZBmzaZCZCXKMHox3nhu6VCuZBzKufAJZCYkxfB3ZAwZDZD
PHONE_NUMBER_ID=720494921152084
WHATSAPP_VERIFY_TOKEN=fitblendz_whatsapp_verify_7c2f4b1e
BARBER_WHATSAPP=+916239514954
EMAIL_HOST=smtp-relay.brevo.com
EMAIL_PORT=587
EMAIL_HOST_USER=bjot404@gmail.com
EMAIL_HOST_PASSWORD=tL7VjqZgIwnTA1dy
DEFAULT_FROM_EMAIL=bjot404@gmail.com
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created with default values")
        print("⚠️  Please update the .env file with your actual credentials")
    
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
    django.setup()
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating database migrations"):
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying database migrations"):
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    # Create sample data
    print("📊 Creating sample data...")
    try:
        from booking.models import Service, WorkingHours
        
        # Create sample services if none exist
        if not Service.objects.exists():
            services_data = [
                {'name': 'Haircut', 'description': 'Professional haircut and styling', 'duration': 30, 'price': 25.00},
                {'name': 'Beard Trim', 'description': 'Beard trimming and shaping', 'duration': 20, 'price': 15.00},
                {'name': 'Haircut + Beard', 'description': 'Complete grooming package', 'duration': 45, 'price': 35.00},
                {'name': 'Hair Wash', 'description': 'Hair washing and conditioning', 'duration': 15, 'price': 10.00},
            ]
            
            for service_data in services_data:
                Service.objects.create(**service_data)
            print("✅ Sample services created")
        
        # Create working hours if none exist
        if not WorkingHours.objects.exists():
            from datetime import time
            
            working_hours_data = [
                {'day': 0, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(18, 0)},  # Monday
                {'day': 1, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(18, 0)},  # Tuesday
                {'day': 2, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(18, 0)},  # Wednesday
                {'day': 3, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(18, 0)},  # Thursday
                {'day': 4, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(18, 0)},  # Friday
                {'day': 5, 'is_open': True, 'open_time': time(9, 0), 'close_time': time(17, 0)},  # Saturday
                {'day': 6, 'is_open': False},  # Sunday
            ]
            
            for hours_data in working_hours_data:
                WorkingHours.objects.create(**hours_data)
            print("✅ Working hours configured")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create sample data: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    
    print("\n📋 Next Steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Create a superuser account:")
    print("   python manage.py createsuperuser")
    print("\n3. Access the admin panel:")
    print("   http://localhost:8000/admin/")
    print("\n4. Test the webhook:")
    print("   python test_webhook.py <ngrok_url> fitblendz_whatsapp_verify_7c2f4b1e")
    print("\n5. Configure WhatsApp Business webhook:")
    print("   - Callback URL: https://your-ngrok-url.ngrok.io/webhook/")
    print("   - Verify Token: fitblendz_whatsapp_verify_7c2f4b1e")
    
    print("\n🚀 Your FitBlendz Pro system is ready to use!")

if __name__ == "__main__":
    setup_project()
