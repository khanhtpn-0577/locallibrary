from django.shortcuts import render, get_object_or_404
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
import datetime
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.forms import RenewBookForm


BOOK_LIST_CONTEXT_NAME = 'book_list'
BOOK_LIST_TEMPLATE = 'catalog/book_list.html'
BOOK_LIST_PAGINATE_BY = 10
DEFAULT_DATE_OF_DEATH = date(2020, 6, 11)


@login_required
def index(request):
    """View function for home page of site."""

    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(
        status=BookInstance.LoanStatus.AVAILABLE).count()

    num_authors = Author.objects.count()

    # Dung sessions dem so lan truy cap
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = BOOK_LIST_CONTEXT_NAME
    template_name = BOOK_LIST_TEMPLATE
    paginate_by = BOOK_LIST_PAGINATE_BY


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()

        context['bookinstances'] = book.bookinstance_set.all()
        context['STATUS_AVAILABLE'] = BookInstance.LoanStatus.AVAILABLE
        context['STATUS_MAINTENANCE'] = BookInstance.LoanStatus.MAINTENANCE
        return context


@login_required
def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = BOOK_LIST_PAGINATE_BY

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status=BookInstance.LoanStatus.ON_LOAN
        ).order_by('due_back')


@permission_required('catalog.can_mark_returned')
def mark_book_returned(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    book_instance.status = BookInstance.LoanStatus.AVAILABLE
    book_instance.save()
    return redirect('my-borrowed')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""

    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


@login_required
def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if book_instance.status == BookInstance.LoanStatus.AVAILABLE:
        book_instance.status = BookInstance.LoanStatus.ON_LOAN
        book_instance.borrower = request.user
        book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        book_instance.save()

    return HttpResponseRedirect(reverse('my-borrowed'))

class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': DEFAULT_DATE_OF_DEATH}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

