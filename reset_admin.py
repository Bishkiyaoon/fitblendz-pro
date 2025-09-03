#!/usr/bin/env python
"""
Reset Admin User Script for FitBlendz Pro
This script will create or reset your admin user
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def reset_admin():
    """Reset or create admin user"""
    try:
        # Check if admin user exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fitblendz.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True
            }
        )
        
        if created:
            print("✅ New admin user created!")
        else:
            print("✅ Admin user already exists, updating...")
        
        # Set new password
        new_password = 'admin123'  # You can change this
        admin_user.password = make_password(new_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.is_active = True
        admin_user.save()
        
        print("🔑 Admin credentials updated successfully!")
        print(f"👤 Username: admin")
        print(f"🔐 Password: {new_password}")
        print(f"📧 Email: {admin_user.email}")
        print("\n🌐 You can now login at:")
        print("   - Custom Admin: http://127.0.0.1:8000/book/admin-login/")
        print("   - Django Admin: http://127.0.0.1:8000/admin/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Resetting Admin User...")
    reset_admin()


