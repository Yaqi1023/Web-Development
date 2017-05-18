from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm
from collection.serializers import AuthorSerializer


class BookList(FormMixin, ListView):
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    @method_decorator(permission_required('collection.can_add_book'))
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

    @method_decorator(permission_required, 'collection.can_add_author')
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


@csrf_exempt
def author_list(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AuthorSerializer(author, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        author.delete()
        return HttpResponse(status=204)
