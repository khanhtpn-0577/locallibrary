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
    path(
        'book/<uuid:pk>/renew/',
        views.renew_book_librarian,
        name='renew-book-librarian'
    ),
    path('borrowed/', views.LoanedBooksByUserListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow-book'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
