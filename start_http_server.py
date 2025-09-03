#!/usr/bin/env python
"""
Simple HTTP server for Django - for immediate access
"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server

def main():
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
    django.setup()
    
    print("🌐 Starting Django with HTTP support...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("🔐 Admin Login: http://localhost:8000/admin-login/")
    print("📊 Admin Dashboard: http://localhost:8000/admin-dashboard/")
    print("\n🚀 Starting server... Press Ctrl+C to stop")
    
    try:
        # Get Django WSGI application
        application = get_wsgi_application()
        
        # Create HTTP server
        server = make_server('localhost', 8000, application)
        
        print("✅ HTTP Server started successfully!")
        print("🌐 Visit: http://localhost:8000")
        print("🔐 Admin Login: http://localhost:8000/admin-login/")
        print("📊 Admin Dashboard: http://localhost:8000/admin-dashboard/")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()

