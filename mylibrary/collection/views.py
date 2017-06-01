from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm
from collection.serializers import AuthorSerializer, BookSerializer


class BookList(FormMixin, ListView):
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        deleted_book = self.request.session.get('deleted_book', False)
        if deleted_book:
            context['deleted_book'] = deleted_book
            del self.request.session['deleted_book']
        return context

    @method_decorator(permission_required('collection.add_book'))
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

    @method_decorator(permission_required('collection.add_author'))
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

    @method_decorator(permission_required('collection.delete_book'))
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        request.session['deleted_book'] = '"{}" ({})'.format(book.title, book.id)
        book.delete()
        return JsonResponse({})
 

class AuthorDetail(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context


class APIAuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class APIBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
