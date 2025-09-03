"""
Custom management command to run Django development server with SSL
"""
import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line
from django.conf import settings
import ssl
import socket
from http.server import HTTPServer
from wsgiref.simple_server import WSGIRequestHandler
import threading
import time

class SSLWSGIRequestHandler(WSGIRequestHandler):
    """Custom request handler for SSL"""
    def get_environ(self):
        env = super().get_environ()
        env['wsgi.url_scheme'] = 'https'
        return env

class SSLWSGIServer(HTTPServer):
    """Custom WSGI server with SSL support"""
    def __init__(self, server_address, RequestHandlerClass, certfile, keyfile):
        super().__init__(server_address, RequestHandlerClass)
        
        # Create SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile, keyfile)
        
        # Wrap socket with SSL
        self.socket = context.wrap_socket(self.socket, server_side=True)

class Command(BaseCommand):
    help = 'Run Django development server with SSL support'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--host',
            default='127.0.0.1',
            help='Host to bind to (default: 127.0.0.1)'
        )
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Port to bind to (default: 8000)'
        )
        parser.add_argument(
            '--cert',
            default='cert.pem',
            help='SSL certificate file (default: cert.pem)'
        )
        parser.add_argument(
            '--key',
            default='key.pem',
            help='SSL private key file (default: key.pem)'
        )
    
    def handle(self, *args, **options):
        host = options['host']
        port = options['port']
        cert_file = options['cert']
        key_file = options['key']
        
        # Check if certificate files exist
        if not os.path.exists(cert_file):
            self.stdout.write(
                self.style.ERROR(f'Certificate file not found: {cert_file}')
            )
            self.stdout.write(
                self.style.WARNING('Run: openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=IN/ST=State/L=City/O=FitBlendz/OU=IT/CN=localhost"')
            )
            return
        
        if not os.path.exists(key_file):
            self.stdout.write(
                self.style.ERROR(f'Private key file not found: {key_file}')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting Django server with SSL on https://{host}:{port}')
        )
        self.stdout.write(f'Certificate: {cert_file}')
        self.stdout.write(f'Private Key: {key_file}')
        self.stdout.write('Press Ctrl+C to stop the server')
        
        try:
            # Import Django WSGI application
            from django.core.wsgi import get_wsgi_application
            application = get_wsgi_application()
            
            # Create SSL server
            server = SSLWSGIServer(
                (host, port),
                SSLWSGIRequestHandler,
                cert_file,
                key_file
            )
            
            # Set WSGI application
            server.set_app(application)
            
            # Start server
            server.serve_forever()
            
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('\nServer stopped.'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error starting server: {e}')
            )
            self.stdout.write(
                self.style.WARNING('Make sure the certificate files are valid and accessible')
            )

