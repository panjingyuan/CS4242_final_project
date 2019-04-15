from django.contrib import admin
from mysite.models import Article, Category, Subcat, Keyword, Profile

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('sitetype', 'title', 'cat', 'datetime')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Subcat)
admin.site.register(Keyword)
admin.site.register(Profile)
