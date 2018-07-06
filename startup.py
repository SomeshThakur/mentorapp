import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = os.getcwd().split('\\')[-1] + '.settings'
django.setup()