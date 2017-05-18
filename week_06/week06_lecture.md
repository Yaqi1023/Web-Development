# Week 6 - REST APIs

This week we will discuss building web applications and APIs that conform to the Representational State Transfer (REST) model and the HTTP protocol.

## REST Principles

***ToDo***

## HTTP Protocol

***ToDo***

### Methods

***ToDo***

### Headers

***ToDo***

### Content Negotiation

***ToDo***

## The Django Rest Framework

Building out a set of views to handle the various HTTP methods, serializations, and content negotiation can be time consuming. Luckily for us, there is a very good package that can do alot of this for you, called the Django REST Framework: http://www.django-rest-framework.org/

### Set Up

First we will need to install it. Preferably, you should include it in a `requirements.txt` file.

```bash
(ENV)$ pip install djangorestframework
```

Once it is installed, you need to add it to the **INSTALLED_APPS** in your `settings.py` file.

```python
# settings.py

INSTALLED_APPS = (
    ...
    'rest_framework',
)
```

Then, add the URL patterns in your `urls.py` file. This is not required, but is useful if you want use the *browseable* API.

```python
# urls.py

urlpatterns = [
    ...
    url(r'^api-auth/', include('rest_framework.urls'))
]
```

First we need to create a serializer to convert our data to a standard interchange format like JSON or XML. Create a new file in your app directory called `serializers.py`. Let's create a serializer for our `Author` model.

```python
# serializers.py

from rest_framework import serializers
from collection.models import Book, Author


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    last_name = serializers.CharField(required=False, allow_blank=True,
        max_length=64)
    first_name = serializers.CharField(required=True, max_length=64)
    birth_year = serializers.IntegerField(required=False, allow_blank=True)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.birth_year = validated_data.get('birth_year', instance.birth_year)
        instance.save()
        return instance
```

The serializer takes you model instance data and prepares it for standard output. You can then pass it to a ***renderer*** to output a specific serialization format. The django rest frameowrk comes with a builtin JSONRenderer. Let's try it out in the command line.

```python
from collection.models import Author
from collection.serializers import AuthorSerializer
from rest_framework.renderers import JSONRenderer

author = Author.objects.filter(last_name='Asimov').first()
serializer = AuthorSerializer(author)
content = JSONRenderer().render(serializer.data)
content
b'{"id":304,"last_name":"Asimov","first_name":" Isaac","birth_year":null}'
```

We can also take in JSON data and convert it back to a Django model.

```python
from django.utils.six import BytesIO
rom rest_framework.parsers import JSONParser

stream = BytesIO(content)
data = JSONParser().parse(stream)
serializer = AuthorSerializer(data=data)
serializer.is_valid()
serializer.validated_data
serializer.save()
<Author: Asimov, Isaac>
```

You can also serialize multiple items at a time:

```python
serializer = AuthorSerializer(Author.objects.all(), many=True)
serializer.data
[OrderedDict([('id', 757), ('last_name', 'Abbott'), ('first_name', ' Edwin A.'), ('birth_year', None)]), OrderedDict([('id', 658), ('last_name', 'Abelson'), ('first_name', ' Harold'), ('birth_year', None)]),
...
```

All of this feels a lot like using Django Forms. The forms package came with special ModelForms for handling routine forms for updating models. Well, the rest framework has the same thing for serializers. A `ModelSerializer` takes out all the redundancy of setting up a serializer based on a model. Let's try using one for the `Book` model.

```python
# serializers.py

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'pub_year', 'isbn', 'rating', 'notes')
```

And that's it. Mush easier huh? But what about that `author` field? That was a ForeignKey field. How did that get handled. You can inspect the fields by print the `repr` of the serializer, like so:

```python
from collection.serializers import BookSerializer
serializer = BookSerializer()
print(repr(serializer))
BookSerializer():
    id = IntegerField(label='ID', read_only=True)
    author = PrimaryKeyRelatedField(allow_null=True, queryset=Author.objects.all(), required=False)
    title = CharField(max_length=256)
    pub_year = IntegerField(allow_null=True, required=False)
    isbn = CharField(allow_blank=True, allow_null=True, max_length=13, required=False)
    rating = ChoiceField(choices=((0, 'Unrated'), (1, 'Hate it'), (2, 'Meh'), (3, 'Nice'), (4, 'Loved it'), (5, 'Masterpiece!')), required=False)
    notes = CharField(allow_blank=True, allow_null=True, required=False, style={'base_template': 'textarea.html'})
```

You can see that `author` was defined as a `PrimaryKeyIntegerField`.

OK, let's create some views to make use of these serializers:

```python
# views.py
# ...
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm
from collection.serializers import AuthorSerializer
# ...

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
```

And now we need to add some urls to point to these views. But let's not overwrite out current urls just yet. Let's put these new views under a subdirectory of our site, called `/api/`.

```python
# urls.py

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail, author_list, author_detail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/authors/$', author_list),
    url('^api/authors/(?P<pk>[0-9]+)/$', author_detail)
]
```

Now test it out. Turn on the dev server and go to http://127.0.0.1:8000/api/authors



