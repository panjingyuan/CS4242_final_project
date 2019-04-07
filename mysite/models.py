# Derived from
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Model representing a category"""
    name = models.CharField(max_length=200, help_text='Article category')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Subcat(models.Model):
    """Model representing a sub-category"""
    name = models.CharField(max_length=200, help_text='Article sub-category')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Article(models.Model):
    """Model representing a specific article."""
    # Meta
    # Foreign Key used because article can only have one author, but authors can have multiple articles
    # Author as a string rather than object because it hasn't been declared yet in the file
    id = models.UUIDField(help_text='Unique article ID')
    title = models.CharField(max_length=200, help_text='Article name')
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(help_text='The given synopsis for the file')
    datetime = models.DateTimeField(help_text = 'Time published')

    # Stats
    views = models.IntegerField(help_text='View #')
    favs  = models.IntegerField(help_text='Favourited #')
    cmnts = models.IntegerField(help_text='Comment #')

    #
    link = models.URLField(help_text='Link to Article')
    img = models.URLField(help_text='Link to image')
    # categories
    cat = models.ForeignKey(Category, help_text='Category this article is related to')
    subcat = models.ManyToManyField(Subcat, help_text='Subcategories this article is related to')


    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('article-detail', args=[str(self.id)])
