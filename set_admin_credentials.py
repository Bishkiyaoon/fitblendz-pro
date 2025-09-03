#!/usr/bin/env python
"""
Set Admin Credentials Script for FitBlendz Pro
Edit the NEW_USERNAME and NEW_PASSWORD variables below, then run this script
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# ========================================
# EDIT THESE VALUES TO YOUR PREFERENCE
# ========================================
NEW_USERNAME = "your_new_username"  # Change this to your desired username
NEW_PASSWORD = "your_new_password"  # Change this to your desired password
# ========================================

def set_admin_credentials():
    """Set admin user credentials"""
    try:
        print("🔧 Setting Admin Credentials for FitBlendz Pro")
        print("=" * 50)
        
        # Validate input
        if not NEW_USERNAME or NEW_USERNAME == "your_new_username":
            print("❌ Please edit the script and set NEW_USERNAME to your desired username!")
            return False
        
        if not NEW_PASSWORD or NEW_PASSWORD == "your_new_password":
            print("❌ Please edit the script and set NEW_PASSWORD to your desired password!")
            return False
        
        print(f"👤 Setting username to: {NEW_USERNAME}")
        print(f"🔐 Setting password to: {NEW_PASSWORD}")
        print()
        
        # Check if username already exists
        if User.objects.filter(username=NEW_USERNAME).exists():
            print(f"❌ Username '{NEW_USERNAME}' already exists!")
            return False
        
        # Delete old admin user if it exists
        old_admin = User.objects.filter(username='admin').first()
        if old_admin:
            old_admin.delete()
            print("🗑️  Old admin user removed")
        
        # Create new admin user
        new_admin = User.objects.create_user(
            username=NEW_USERNAME,
            email=f'{NEW_USERNAME}@fitblendz.com',
            password=NEW_PASSWORD,
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print("✅ New admin user created successfully!")
        print(f"👤 Username: {NEW_USERNAME}")
        print(f"🔐 Password: {NEW_PASSWORD}")
        print(f"📧 Email: {new_admin.email}")
        print("\n🌐 You can now login at:")
        print("   - Custom Admin: http://127.0.0.1:8000/book/admin-login/")
        print("   - Django Admin: http://127.0.0.1:8000/admin/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    set_admin_credentials()







