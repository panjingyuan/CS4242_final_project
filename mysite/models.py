# Derived from
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
from django.db import models

class Article(models.Model):
    """Model representing a how-to article"""
    name = models.CharField(max_length=200, help_text='Name of the article')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
