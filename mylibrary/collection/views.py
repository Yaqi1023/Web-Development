from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm


class BookList(FormMixin, ListView):
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('book_list')


class AuthorList(FormMixin, ListView):
    model = Author
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        author = Author()
        author.last_name = form.cleaned_data['last_name']
        author.first_name = form.cleaned_data['first_name']
        author.birth_year = form.cleaned_data['birth_year']
        author.save()
        return super(AuthorList, self).form_valid(form)

    def get_success_url(self):
        return reverse('author_list')



class BookDetail(DetailView):
    model = Book
 

class AuthorDetail(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context
