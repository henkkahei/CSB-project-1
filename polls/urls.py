from django.urls import include, path

from django.contrib.auth.decorators import login_required
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:qid>/vote/", views.vote, name="vote"),
    path("search/", views.SearchView.as_view(), name="search"),
]