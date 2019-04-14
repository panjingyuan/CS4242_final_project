from django.shortcuts import render
from django.contrib.auth.models import User
from django.views import generic

from mysite.models import Article, Category, Subcat

def index(request):
    """View function for index"""
    context = {}
    return render(request, "index.html", context=context)

def stats(request):
    """View function for stats of site."""

    # Generate counts of some of the main objects
    num_articles = Article.objects.all().count()
    users = User.objects.all()
    num_users = users.count()
    num_super = 0
    for item in users:
        print(item)
        if item.is_superuser:
            num_super += 1
    num_categories = Category.objects.all().count()
    num_subcats = Subcat.objects.all().count()
    num_zero = 0

    # realise these values as variables
    context = {
        'num_articles': num_articles,
        'num_users': num_users,
        'num_super': num_super,
        'num_categories': num_categories,
        'num_subcats': num_subcats,
        'num_zero': num_zero,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'site_base_stats.html', context=context)

class UserListView(generic.ListView):
    model = User
    paginate_by = 10
    context_object_name = 'user_list'
    queryset = User.objects.all()
    user_list = User.objects.all()
    print(queryset)
    template_name = 'site_base_users.html'  # Specify your own template name/location

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    queryset = Article.objects.all()
    articles = Article.objects.all()
    print(queryset)
    template_name = 'site_base_articles.html'  # Specify your own template name/location
