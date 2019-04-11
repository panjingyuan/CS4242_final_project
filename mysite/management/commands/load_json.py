import json
import os, sys
import django
from django.conf import settings
from django.core.management.base import BaseCommand

from mysite.models import Article, Category, Subcat

print("Hello World! From manage.py!")
