from django.contrib import admin
from mysite.models import Article, Category, Subcat, Keyword

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('sitetype', 'title', 'cat', 'datetime')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Subcat)
admin.site.register(Keyword)
