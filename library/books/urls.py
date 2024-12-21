from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookDeleteView, BookUpdateView
urlpatterns = [
    path("", BookListView.as_view(), name="book-list"),
    path("<int:pk>/", BookDetailView.as_view(), name="book-details"),
    path("create/", BookCreateView.as_view(), name="book-create"),
    path("delete/<int:pk>", BookDeleteView.as_view(), name="book-delete"),
    path("update/<int:pk>", BookUpdateView.as_view(), name="book-update"),


]