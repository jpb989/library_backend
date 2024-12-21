from django.urls import path
from .views import AuthorListView, AuthorDetailView, AuthorCreateView, AuthorDeleteView, AuthorUpdateView, \
                   BookListView, BookDetailView, BookCreateView, BookDeleteView, BookUpdateView, \
                   BorrowBookView, ReturnBookView, ReportView
urlpatterns = [
    path("author/", AuthorListView.as_view(), name="author-list"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-details"),
    path("author/create/", AuthorCreateView.as_view(), name="author-create"),
    path("author/delete/<int:pk>", AuthorDeleteView.as_view(), name="author-delete"),
    path("author/update/<int:pk>", AuthorUpdateView.as_view(), name="author-update"),


    path("book/", BookListView.as_view(), name="book-list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book-details"),
    path("book/create/", BookCreateView.as_view(), name="book-create"),
    path("book/delete/<int:pk>", BookDeleteView.as_view(), name="book-delete"),
    path("book/update/<int:pk>", BookUpdateView.as_view(), name="book-update"),


    path('borrow/', BorrowBookView.as_view(), name='borrow-book'),
    path('borrow/<int:pk>/return/', ReturnBookView.as_view(), name='return-book'),
    
    path("reports/", ReportView.as_view(), name="reports"),

]