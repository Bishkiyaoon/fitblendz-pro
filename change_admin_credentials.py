#!/usr/bin/env python
"""
Change Admin Credentials Script for FitBlendz Pro
This script allows you to set custom admin username and password
"""

import os
import django
import getpass

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def change_admin_credentials():
    """Change admin user credentials"""
    try:
        print("🔧 Change Admin Credentials for FitBlendz Pro")
        print("=" * 50)
        
        # Get new credentials from user
        new_username = input("Enter new admin username: ").strip()
        if not new_username:
            print("❌ Username cannot be empty!")
            return False
        
        new_password = getpass.getpass("Enter new admin password: ").strip()
        if not new_password:
            print("❌ Password cannot be empty!")
            return False
        
        confirm_password = getpass.getpass("Confirm new admin password: ").strip()
        if new_password != confirm_password:
            print("❌ Passwords do not match!")
            return False
        
        # Check if username already exists
        if User.objects.filter(username=new_username).exists():
            print(f"❌ Username '{new_username}' already exists!")
            return False
        
        # Delete old admin user if it exists
        old_admin = User.objects.filter(username='admin').first()
        if old_admin:
            old_admin.delete()
            print("🗑️  Old admin user removed")
        
        # Create new admin user
        new_admin = User.objects.create_user(
            username=new_username,
            email=f'{new_username}@fitblendz.com',
            password=new_password,
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print("✅ New admin user created successfully!")
        print(f"👤 Username: {new_username}")
        print(f"🔐 Password: {new_password}")
        print(f"📧 Email: {new_admin.email}")
        print("\n🌐 You can now login at:")
        print("   - Custom Admin: http://127.0.0.1:8000/book/admin-login/")
        print("   - Django Admin: http://127.0.0.1:8000/admin/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    change_admin_credentials()

