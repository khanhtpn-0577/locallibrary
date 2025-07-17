from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

BOOK_LIST_CONTEXT_NAME = 'book_list'
BOOK_LIST_TEMPLATE = 'catalog/book_list.html'
BOOK_LIST_PAGINATE_BY = 10


def index(request):
    """View function for home page of site."""

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(
        status=BookInstance.LoanStatus.AVAILABLE).count()

    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = BOOK_LIST_CONTEXT_NAME
    template_name = BOOK_LIST_TEMPLATE
    paginate_by = BOOK_LIST_PAGINATE_BY


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        context['bookinstances'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = BookInstance.LoanStatus.AVAILABLE
        context['STATUS_MAINTENANCE'] = BookInstance.LoanStatus.MAINTENANCE
        return context


def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})
