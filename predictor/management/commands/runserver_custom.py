from django.core.management.base import BaseCommand
from django.core.wsgi import get_wsgi_application
from core.custom_server import run

class Command(BaseCommand):
    help = 'Runs the server with a custom configuration that bypasses hostname issues'

    def handle(self, *args, **options):
        self.stdout.write('Starting custom development server...')
        application = get_wsgi_application()
        run('127.0.0.1', 8000, application) 