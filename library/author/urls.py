from django.urls import path
from .views import AuthorListView, AuthorDetailView, AuthorCreateView, AuthorDeleteView, AuthorUpdateView

urlpatterns = [
    path("author/", AuthorListView.as_view(), name="author-list"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-details"),
    path("author/create/", AuthorCreateView.as_view(), name="author-create"),
    path("author/delete/<int:pk>", AuthorDeleteView.as_view(), name="author-delete"),
    path("author/update/<int:pk>", AuthorUpdateView.as_view(), name="author-update"),
]