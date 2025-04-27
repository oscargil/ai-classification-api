from django.core.management.commands.runserver import Command as RunserverCommand
from django.core.servers import basehttp
import socket

# Monkey patch socket.getfqdn to return a simple string
def fixed_getfqdn(name):
    return '127.0.0.1'

socket.getfqdn = fixed_getfqdn

class Command(RunserverCommand):
    help = 'Runs the server with a fix for hostname resolution issues' 