#!/usr/bin/env python
"""
Working SSL server for Django - compatible with modern Python versions
"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application
import ssl
from wsgiref.simple_server import make_server, WSGIRequestHandler

class SSLWSGIRequestHandler(WSGIRequestHandler):
    """Custom request handler for SSL"""
    def get_environ(self):
        env = super().get_environ()
        env['wsgi.url_scheme'] = 'https'
        return env

def main():
    # Setup Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitblendz_pro.settings')
    django.setup()
    
    # Check if certificate files exist
    cert_file = 'cert.pem'
    key_file = 'key.pem'
    
    if not os.path.exists(cert_file):
        print(f"❌ Certificate file not found: {cert_file}")
        print("Run: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj \"/C=IN/ST=State/L=City/O=FitBlendz/OU=IT/CN=localhost\"")
        return
    
    if not os.path.exists(key_file):
        print(f"❌ Private key file not found: {key_file}")
        return
    
    print("🔒 Starting Django with SSL support...")
    print(f"📜 Certificate: {cert_file}")
    print(f"🔑 Private Key: {key_file}")
    print("🌐 Server will be available at: https://localhost:8000")
    print("⚠️  Note: This is a self-signed certificate. Your browser may show a security warning.")
    print("   Click 'Advanced' and 'Proceed to localhost (unsafe)' to continue.")
    print("\n🚀 Starting server... Press Ctrl+C to stop")
    
    try:
        # Get Django WSGI application
        application = get_wsgi_application()
        
        # Create server
        server = make_server('localhost', 8000, application)
        
        # Wrap with SSL using modern SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        
        # Wrap socket with SSL
        server.socket = context.wrap_socket(server.socket, server_side=True)
        
        print("✅ Server started successfully!")
        print("🌐 Visit: https://localhost:8000")
        print("🔐 Admin Login: https://localhost:8000/admin-login/")
        print("📊 Admin Dashboard: https://localhost:8000/admin-dashboard/")
        
        # Start server
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure certificate files exist")
        print("   2. Check if port 8000 is available")
        print("   3. Try a different port")

if __name__ == "__main__":
    main()

