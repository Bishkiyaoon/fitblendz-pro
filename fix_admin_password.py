#!/usr/bin/env python
"""
Fix Admin Password Script for FitBlendz Pro
This script will create a fresh admin user with a known password
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def fix_admin_password():
    """Create a fresh admin user with known password"""
    try:
        print("🔧 Fixing Admin Password for FitBlendz Pro")
        print("=" * 50)
        
        # Delete all existing admin users
        User.objects.filter(is_staff=True).delete()
        print("🗑️  Deleted all existing admin users")
        
        # Create fresh admin user
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@fitblendz.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        
        print("✅ Fresh admin user created successfully!")
        print(f"👤 Username: admin")
        print(f"🔐 Password: admin123")
        print(f"📧 Email: {admin_user.email}")
        print(f"🔑 Staff: {admin_user.is_staff}")
        print(f"🔑 Superuser: {admin_user.is_superuser}")
        print(f"🔑 Active: {admin_user.is_active}")
        
        # Test the password
        from django.contrib.auth import authenticate
        test_user = authenticate(username='admin', password='admin123')
        if test_user:
            print("✅ Password verification successful!")
        else:
            print("❌ Password verification failed!")
        
        print("\n🌐 You can now login at:")
        print("   - Custom Admin: http://127.0.0.1:8000/book/admin-login/")
        print("   - Django Admin: http://127.0.0.1:8000/admin/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_admin_password()
