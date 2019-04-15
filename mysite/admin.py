from django.contrib import admin
from mysite.models import Article, Category, Subcat

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'sitetype', 'datetime', 'cat')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Subcat)
