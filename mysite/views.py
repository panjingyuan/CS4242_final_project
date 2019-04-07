from django.shortcuts import render
import models

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_articles = Article.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_articles': num_articles,
        'num_users': num_users,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
