from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views import generic
import operator

from mysite.models import Article, Category, Subcat, Profile

def index(request):
    """View function for index"""
    context = {}
    return render(request, "index.html", context=context)

def stats(request):
    """View function for stats of site."""

    # Generate counts of some of the main objects
    num_articles = Article.objects.all().count()
    users = Profile.objects.all()
    num_users = users.count()
    num_categories = Category.objects.all().count()
    num_subcats = Subcat.objects.all().count()
    num_zero = 0

    # realise these values as variables
    context = {
        'num_articles': num_articles,
        'num_users': num_users,
        'num_categories': num_categories,
        'num_subcats': num_subcats,
        'num_zero': num_zero,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'site_base_stats.html', context=context)

def profile(request, pk):
    """View function for profile."""

    profile = get_object_or_404(Profile, pk=pk)
    context = {
        'profile': profile
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'site_base_userdetail.html', context=context)

def article(request, pk):
    """View function for articles."""

    article = get_object_or_404(Article, pk=pk)
    context = {
        'article': article
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'site_base_articledetail.html', context=context)

class UserListView(generic.ListView):
    model = Profile
    paginate_by = 20
    context_object_name = 'user_list'
    queryset = Profile.objects.all()
    user_list = Profile.objects.all()
    #print(queryset)
    template_name = 'site_base_users.html'  # Specify your own template name/location

class ArticleListView(generic.ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    queryset = Article.objects.all()
    articles = Article.objects.all()
    #print(queryset)
    template_name = 'site_base_articles.html'  # Specify your own template name/location

class CatListView(generic.ListView):
    model = Category
    paginate_by = 12
    context_object_name = 'categories'
    queryset = Category.objects.all()
    categories = Category.objects.all()
    #print(queryset)
    template_name = 'site_base_cats.html'  # Specify your own template name/location

class CatArtList(generic.ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['category'] = self.category
        return context

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        return Article.objects.filter(cat=self.category)

    template_name = 'site_base_cat_articles.html'

class QueryList(generic.ListView):
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'site_base_search.html'
