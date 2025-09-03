#!/usr/bin/env python3
"""
Performance Monitoring Script for FitBlendz Pro
This script monitors database performance and provides optimization suggestions
"""

import os
import sys
import django
import time
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
django.setup()

from django.db import connection
from django.conf import settings
from django.utils import timezone
from booking.models import Appointment, Service
from django.db.models import Count, Q
import psutil

def check_database_performance():
    """Check database performance metrics"""
    print("📊 Database Performance Analysis")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        # Check table sizes
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    attname,
                    n_distinct,
                    correlation
                FROM pg_stats 
                WHERE schemaname = 'public' 
                AND tablename IN ('booking_appointment', 'booking_service')
                ORDER BY tablename, attname;
            """)
            stats = cursor.fetchall()
            
            print("📈 PostgreSQL Statistics:")
            for stat in stats:
                print(f"   Table: {stat[1]}, Column: {stat[2]}, Distinct: {stat[3]}, Correlation: {stat[4]}")
        
        # Check slow queries (if available)
        try:
            cursor.execute("SHOW log_min_duration_statement;")
            log_duration = cursor.fetchone()
            print(f"📝 Slow query logging: {log_duration[0] if log_duration else 'Not configured'}")
        except:
            print("📝 Slow query logging: Not available (SQLite)")

def check_model_performance():
    """Check model query performance"""
    print("\n🔍 Model Performance Analysis")
    print("-" * 40)
    
    # Test common queries
    queries_to_test = [
        ("All appointments", lambda: Appointment.objects.all()),
        ("Appointments with service", lambda: Appointment.objects.select_related('service').all()),
        ("Pending appointments", lambda: Appointment.objects.filter(status='pending')),
        ("Today's appointments", lambda: Appointment.objects.filter(date=timezone.now().date())),
        ("Appointments by service", lambda: Appointment.objects.filter(service__name__icontains='Hair')),
    ]
    
    for name, query_func in queries_to_test:
        start_time = time.time()
        try:
            result = query_func()
            count = result.count() if hasattr(result, 'count') else len(list(result))
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            
            status = "✅" if duration < 100 else "⚠️" if duration < 500 else "❌"
            print(f"   {status} {name}: {count} records, {duration:.2f}ms")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")

def check_system_resources():
    """Check system resource usage"""
    print("\n💻 System Resource Usage")
    print("-" * 40)
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"🖥️  CPU Usage: {cpu_percent}%")
    
    # Memory usage
    memory = psutil.virtual_memory()
    print(f"🧠 Memory Usage: {memory.percent}% ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
    
    # Disk usage
    disk = psutil.disk_usage('/')
    print(f"💾 Disk Usage: {disk.percent}% ({disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB)")
    
    # Database file size (if SQLite)
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / 1024**2  # MB
            print(f"🗄️  Database Size: {db_size:.2f}MB")

def check_database_indexes():
    """Check database indexes"""
    print("\n📋 Database Index Analysis")
    print("-" * 40)
    
    with connection.cursor() as cursor:
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            cursor.execute("""
                SELECT 
                    indexname,
                    tablename,
                    indexdef
                FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename IN ('booking_appointment', 'booking_service')
                ORDER BY tablename, indexname;
            """)
            indexes = cursor.fetchall()
            
            print("📊 PostgreSQL Indexes:")
            for index in indexes:
                print(f"   {index[1]}.{index[0]}: {index[2][:80]}...")
        else:
            print("📊 SQLite Indexes:")
            cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND sql IS NOT NULL;")
            indexes = cursor.fetchall()
            for index in indexes:
                print(f"   {index[0]}: {index[1][:80]}...")

def generate_recommendations():
    """Generate performance recommendations"""
    print("\n💡 Performance Recommendations")
    print("-" * 40)
    
    recommendations = []
    
    # Check database engine
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
        recommendations.append("🔄 Consider migrating to PostgreSQL for better performance")
    
    # Check DEBUG mode
    if settings.DEBUG:
        recommendations.append("🔧 Set DEBUG=False in production for better performance")
    
    # Check caching
    if not hasattr(settings, 'CACHES') or settings.CACHES['default']['BACKEND'] == 'django.core.cache.backends.dummy.DummyCache':
        recommendations.append("⚡ Enable caching for better performance")
    
    # Check database connection pooling
    if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
        conn_max_age = settings.DATABASES['default'].get('CONN_MAX_AGE', 0)
        if conn_max_age == 0:
            recommendations.append("🔗 Enable database connection pooling (CONN_MAX_AGE)")
    
    # Check for missing indexes
    with connection.cursor() as cursor:
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.postgresql':
            cursor.execute("""
                SELECT COUNT(*) FROM pg_indexes 
                WHERE schemaname = 'public' 
                AND tablename = 'booking_appointment';
            """)
            index_count = cursor.fetchone()[0]
            if index_count < 5:
                recommendations.append("📊 Add more database indexes for better query performance")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ No immediate optimizations needed!")

def main():
    """Main performance monitoring function"""
    print("🚀 FitBlendz Pro Performance Monitor")
    print("=" * 50)
    
    try:
        check_database_performance()
        check_model_performance()
        check_system_resources()
        check_database_indexes()
        generate_recommendations()
        
        print("\n🎉 Performance analysis completed!")
        print("\n📋 Regular monitoring tips:")
        print("1. Run this script weekly to monitor performance")
        print("2. Monitor database size growth")
        print("3. Check for slow queries in production")
        print("4. Monitor system resource usage")
        print("5. Review and optimize database indexes regularly")
        
    except Exception as e:
        print(f"❌ Performance monitoring failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
