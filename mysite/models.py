# Derived from
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """Model representing a category"""
    name = models.CharField(primary_key=True, max_length=200, help_text='Article category')

    @classmethod
    def create(cls, name):
        cls.name = name
        return Category

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Subcat(models.Model):
    """Model representing a sub-category"""
    name = models.CharField(primary_key=True,max_length=200, help_text='Article sub-category')

    @classmethod
    def create(cls, name):
        cls.name = name
        return Subcat

    class Meta:
        verbose_name_plural = "subcategories"

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Keyword(models.Model):
    """Model representing a keyword"""
    name = models.CharField(primary_key=True,max_length=200, help_text='Keywords')

    @classmethod
    def create(cls, name):
        cls.name = name
        return Keyword

    class Meta:
        verbose_name_plural = "keywords"

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Article(models.Model):
    """Model representing a specific article."""
    #the url is the key for the article
    page_url = models.URLField(primary_key = True, help_text='Link to Article', null = False)

    # Meta
    title = models.CharField(max_length=200, help_text='Article name')
    author = models.CharField(max_length=200, help_text='Author name', null = True)
    summary = models.TextField(help_text='The given synopsis for the file', null = True)
    datetime = models.DateTimeField(help_text = 'Time published', null = True)

    # Stats
    views = models.IntegerField(help_text='View #', null = True)
    favs  = models.IntegerField(help_text='Favourited #', null = True)
    cmnts = models.IntegerField(help_text='Comment #', null = True)

    # Meta info
    SITES = [("IN","Instructables"),
            ("WH","WikiHow")]
    sitetype = models.CharField(max_length = 200, help_text='Instructables or WikiHow', choices=SITES, default="1", null = True)
    img = models.URLField(help_text='Link to image', null = True)

    # categories
    cat = models.ForeignKey(Category, on_delete=models.SET_NULL, help_text='Category this article is related to', null = True)
    subcat = models.ForeignKey(Subcat, on_delete=models.SET_NULL, help_text='Subcategories this article is related to', null = True)
    keyword = models.ManyToManyField(Keyword, help_text='Keywords this article is related to')

    class Meta:
        ordering = ['-datetime']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('article-detail', args=[str(self.id)])

class Profile(models.Model):
    """Model representing a profile"""
    name = models.CharField(primary_key = True, max_length = 80, help_text = 'User name', default = "Unnamed", null = False)
    view_count = models.IntegerField(help_text='the number of articles this user has viewed', default = 0)
    viewedOne = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="Last1")
    viewedTwo = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="Last2")
    viewedThree = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="Last3")
    viewedFour = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="Last4")
    viewedFive = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, related_name="Last5")

    def __str__(self):
        return self.name

    def _add_view(self, article):
        modulo = self.view_count % 5 + 1
        if modulo == 1:
            self.viewedOne = article
        elif modulo == 2:
            self.viewedTwo = article
        elif modulo == 3:
            self.viewedThree = article
        elif modulo == 4:
            self.viewedFour = article
        else:
            self.viewedFive = article
        self.view_count += 1

    def get_all_keywords(self):
        view_list = [self.viewedOne, self.viewedTwo, self.viewedThree, self.viewedFour, self.viewedFive]
        keywords = []
        for item in view_list:
            if item:
                for keyword in item["keyword"]:
                    keywords.extend(keyword)
        return keywords
