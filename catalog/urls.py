from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    re_path(
        r'^book/(?P<pk>\d+)$',
        views.BookDetailView.as_view(),
        name='book-detail'
    ),
    path(
        'mybooks/',
        views.LoanedBooksByUserListView.as_view(),
        name='my-borrowed'
    ),
    path(
        'bookinstance/<uuid:pk>/return/',
        views.mark_book_returned,
        name='mark-returned'
    ),
]
