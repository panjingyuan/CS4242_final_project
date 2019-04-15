from django.conf import settings

from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from . import views

from django.contrib import admin


urlpatterns = [
    path("", views.index, name="home"),
#    path("", TemplateView.as_view(template_name="homepage.html"), name="home"),
    path("users/",views.UserListView.as_view(),name="users"),
    path("articles/",views.ArticleListView.as_view(),name="articles"),
    path("categories/",views.CatListView.as_view(),name="categories"),
    path("stats/", views.stats, name="stats"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("articles/<category>", views.CatArtList.as_view(), name= "catart"),
    path("users/<str:pk>", views.profile, name= "profile"),
    path("search", views.QueryList.as_view(), name= "search")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
