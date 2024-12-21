from django.urls import path
from .views import BorrowBookView, ReturnBookView

urlpatterns = [    
    path('', BorrowBookView.as_view(), name='borrow-book'),
    path('<int:pk>/return/', ReturnBookView.as_view(), name='return-book'),


]
