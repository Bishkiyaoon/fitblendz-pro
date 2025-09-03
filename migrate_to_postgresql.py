#!/usr/bin/env python3
"""
PostgreSQL Migration Script for FitBlendz Pro
This script helps migrate from SQLite to PostgreSQL
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.conf import settings
from django.db import connection
import subprocess

def check_postgresql_connection():
    """Check if PostgreSQL connection is working"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ PostgreSQL connection successful!")
            print(f"   Version: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_database_migration():
    """Create database migrations"""
    print("🔄 Creating database migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Migrations created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create migrations: {e}")
        return False

def run_migrations():
    """Run database migrations"""
    print("🚀 Running database migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to run migrations: {e}")
        return False

def create_superuser():
    """Create superuser if needed"""
    print("👤 Creating superuser...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("✅ Superuser created successfully!")
        else:
            print("ℹ️  Superuser already exists, skipping...")
        return True
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

def backup_sqlite_data():
    """Backup SQLite data before migration"""
    print("💾 Backing up SQLite data...")
    try:
        import shutil
        from pathlib import Path
        
        sqlite_file = Path('db.sqlite3')
        if sqlite_file.exists():
            backup_file = Path('db.sqlite3.backup')
            shutil.copy2(sqlite_file, backup_file)
            print(f"✅ SQLite data backed up to {backup_file}")
            return True
        else:
            print("ℹ️  No SQLite database found, skipping backup...")
            return True
    except Exception as e:
        print(f"❌ Failed to backup SQLite data: {e}")
        return False

def main():
    """Main migration process"""
    print("🚀 FitBlendz Pro PostgreSQL Migration")
    print("=" * 50)
    
    # Check if we're in production mode
    if settings.DEBUG:
        print("⚠️  WARNING: You're in DEBUG mode. Make sure to set DEBUG=False for production!")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Migration cancelled.")
            return
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Migration failed at requirements installation")
        return
    
    # Step 2: Backup SQLite data
    if not backup_sqlite_data():
        print("❌ Migration failed at backup step")
        return
    
    # Step 3: Check PostgreSQL connection
    if not check_postgresql_connection():
        print("❌ Migration failed at PostgreSQL connection check")
        print("\n🔧 Troubleshooting tips:")
        print("1. Make sure PostgreSQL is installed and running")
        print("2. Check your database credentials in environment variables:")
        print("   - DB_NAME")
        print("   - DB_USER") 
        print("   - DB_PASSWORD")
        print("   - DB_HOST")
        print("   - DB_PORT")
        print("3. Create the database if it doesn't exist:")
        print("   createdb fitblendz_pro")
        return
    
    # Step 4: Create migrations
    if not create_database_migration():
        print("❌ Migration failed at migration creation")
        return
    
    # Step 5: Run migrations
    if not run_migrations():
        print("❌ Migration failed at migration execution")
        return
    
    # Step 6: Create superuser
    if not create_superuser():
        print("❌ Migration failed at superuser creation")
        return
    
    print("\n🎉 PostgreSQL migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Set DEBUG=False in your settings")
    print("2. Update your environment variables for production")
    print("3. Test your application thoroughly")
    print("4. Set up proper backup procedures")
    print("5. Configure your web server (nginx/apache)")
    print("6. Set up SSL certificates")
    
    print("\n🔧 Production environment variables needed:")
    print("DEBUG=False")
    print("DB_NAME=fitblendz_pro")
    print("DB_USER=your_db_user")
    print("DB_PASSWORD=your_secure_password")
    print("DB_HOST=localhost")
    print("DB_PORT=5432")
    print("SECRET_KEY=your-secure-secret-key")
    print("ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com")

if __name__ == "__main__":
    main()

