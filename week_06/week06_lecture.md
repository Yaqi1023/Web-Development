# Week 6 - REST APIs

This week we will discuss building web applications and APIs that conform to the Representational State Transfer (REST) model and the HTTP protocol.

## REST Principles

1. Client-Server

    - Separation of concerns
    - Improves portability across platforms
    - Improves scalability by reducing workload on server
    - Enables independent development.

2. Stateless

    - Communication between client and server conatins all information necesary to perform request
    - Session state held on client (can be moved to a database by the server)

3. Cacheable

    - Improves performance
    - Puts constraints on server behavior (don't give out different resources under the same URL)

4. Layered

    - Components only talk to the components directly above or below them in the "stack"
    - e.g. a client does not talk directly to a database
    - Enables better scalability via load-balancers, caches, etc.
    - Separates concerns

5. Code on Demand

    - Serves can extend functionality of a client by delivering executable code
    - e.g JavaScript or Java applets
    - optional, cannot always be relid upon

6. Uniform Interface

    - Simplifies architecture
    - Enables independent development
    - The four constraints of the REST uniform interface
        1. Identification of resources
            - Individual resources are identified in requests (URIs)
            - ***Resources*** are conceptually different than ***representation*** of those resources.
                - e.g. A single document resource may have multiple format representations (HTML, XML, PDF)
        2. Manipulation of resources through representations
            - Each representation, along with the metadata, is sufficient to modify or delete the resource
        3. Self-descriptive messages
            - Metadata (in the form of HTTP Headers) describe how to process the resource
            - e.g. a MIME type signifies if the representation is text, html, json, etc.
        4. Hypermedia as the engine of application state (HATEOAS)
            - The server should provide ***hyperlinks*** to nested resources and functions
            - Simple IDs are not sufficient

## HTTP Protocol

The REST concept was developed in parallel with HTTP/1.1. The HTTP methods and headers enable RESTful component behavior between clients and servers.

### Methods

We looked at these last week.

To review, here is a table (from Wikipedia: https://en.wikipedia.org/wiki/Representational_state_transfer)

Uniform Resource Locator (URL) | GET | PUT | POST | DELETE
-------------------------------|-----|-----|------|-------
Collection, such as http://example.com/cars/ | **List** the URIs and perhaps other details of the collection's members. | **Replace** the entire collection with another collection. | **Create** a new entry in the collection. The new entry's URI is assigned automatically and is usually returned by the operation. |  **Delete** the entire collection.
Element, such as http://example.com/cars/17 | **Retrieve** a representation of the addressed member of the collection, expressed in an appropriate Internet media type. | **Replace** the addressed member of the collection, or if it does not exist, create it. | Not generally used. Treat the addressed member as a collection in its own right and create a new entry within it. *Could be used for a resource that has it's own collection of resource (likely of another type)* | **Delete** the addressed member of the collection.

### Headers

Some commonly seen HTTP Headers from a ***client***

Header name | Description | Example
------------|-------------|--------
Accept | Content-Types that are acceptable for the response. See Content negotiation. | Accept: text/plain  
Accept-Charset | Character sets that are acceptable. | Accept-Charset: utf-8
Accept-Encoding | List of acceptable encodings. See HTTP compression. | Accept-Encoding: gzip, deflate
Accept-Language | List of acceptable human languages for response. See Content negotiation. | Accept-Language: en-US
Content-Type | The MIME type of the body of the request (used with POST and PUT requests). | Content-Type: application/x-www-form-urlencoded
Cookie | An HTTP cookie previously sent by the server with Set-Cookie (below). | Cookie: $Version=1; Skin=new;
User-Agent | The user agent string of the user agent. | User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0

Some commonly seen HTTP Headers from a ***server***

Header name | Description | Example
------------|-------------|--------
Age | The age the object has been in a proxy cache in seconds | Age: 12
Content-Disposition | An opportunity to raise a "File Download" dialogue box for a known MIME type with binary format or suggest a filename for dynamic content. Quotes are necessary with special characters. | Content-Disposition: attachment; filename="fname.ext"
ETag | An identifier for a specific version of a resource, often a message digest |  ETag: "737060cd8c284d8af7ad3082f209582d"
Expires | Gives the date/time after which the response is considered stale (in "HTTP-date" format as defined by RFC 7231) | Expires: Thu, 01 Dec 1994 16:00:00 GMT
Pragma  | Implementation-specific fields that may have various effects anywhere along the request-response chain. | Pragma: no-cache
Set-Cookie  | An HTTP cookie  | Set-Cookie: UserID=JohnDoe; Max-Age=3600; Version=1
Vary | Tells downstream proxies how to match future request headers to decide whether the cached response can be used rather than requesting a fresh one from the origin server. | Vary: Accept-Language

For a complete list of standard and common non-standard headers, see: https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

### Content Negotiation

Since a resource can have multiple representations, how does the server decide which one to send? It can have an internal algorithm to set its default preference. However, it can also adjust to each client request. This is called *proactive* content negotiation. A client can influence this decision by sending HTTP Headers that declare what it would prefer. This is often performed via the `Accept` headers. A client can request a document in JSON format via `Accept: application/json`. However, the response will be JSON only if the server is capable of producing JSON. It may return XML or HTML instead if that is all that it is capable of delivering.

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

### Serializers

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
# command line
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
# command line
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
# command line
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

### Views

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

OK, that worked for our `Author` model. Now let's try out using class-based views instead for the `Book` model. Add the following to your `views.py` file.

```python
# views.py

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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm
from collection.serializers import AuthorSerializer, BookSerializer

# ...

class BookList(APIView):

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

Now add the routes to `urls.py`. Let's also make use of the framework's format extension helper. This will enable us to simply add a `.html` or `.json` to the end of the URL to signify which format we want. Without this we would have to signify that preference in the `Accept` HTTP header.

```python
# urls.py

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail
from collection.views import author_list, author_detail, APIBookList, APIBookDetail

api_urlpatterns = [
    url('^authors/$', author_list),
    url('^authors/(?P<pk>[0-9]+)/$', author_detail),
    url('^books/$', APIBookList.as_view()),
    url('^books/(?P<pk>[0-9]+)/$', APIBookDetail.as_view()),
]

api_urlpatterns = format_suffix_patterns(api_urlpatterns, allowed=['json', 'html'])

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/', include(api_urlpatterns))    
]
```

Now try looking at the books list and an individual book resource:
- http://127.0.0.1:8000/api/books.json
- http://127.0.0.1:8000/api/books/123.json

Well, that worked nicely. But of course, there is a shortcut to what we just did. You can use the generic class-based view to create a standard resource API with a ***list view*** where you can `GET` a list of resources or `POST` a new resource and a ***detail view*** where you can GET details and make changes via `POST`, `PUT`, `PATCH`, and `DELETE`.

Let's redo our functional views for the `Author` model with the generic views.

```python
# views.py
from rest_framework import generics

# ...

class APIAuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class APIAuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

So few lines of code!

And now, update the `urls.py`

```python
# urls.py

# ...
from collection.views import APIAuthorList, APIAuthorDetail, APIBookList, APIBookDetail

api_urlpatterns = [
    url('^authors/$', APIBookList.as_view()),
    url('^authors/(?P<pk>[0-9]+)/$', APIAuthorDetail.as_view()),

# ...
```

Our api endpoint for authors should still work fine.
- http://127.0.0.1:8000/api/authors.json
- http://127.0.0.1:8000/api/authors/45.json

Perefecto!

### Hyperlinking between models

Our book data has the primary key for the author. But the data for the author does not list the related books. Also, wouldn't it be nice if we got the actual url instead of just the ID for related fields? Let's enable that!

First, we need to add a `related_name` attribute to the `author` field of our `Book` model.

```python
# models.py

# ...
    author = models.ForeignKey(Author, null=True, related_name='books')
```

Now, let's update our `AuthorSerializer`

```python
# serializers.py

from rest_framework import serializers
from collection.models import Book, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True,
        queryset=Book.objects.all(), view_name='api_book_detail', format='html')
    url = serializers.HyperlinkedIdentityField(view_name='api_author_detail')

    class Meta:
        model = Author
        fields = ('url', 'id', 'last_name', 'first_name', 'birth_year', 'books')


class BookSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='api_author_detail', format='html')
    url = serializers.HyperlinkedIdentityField(view_name='api_book_detail')

    class Meta:
        model = Book
        fields = ('url', 'id', 'author', 'title', 'pub_year', 'isbn', 'rating', 'notes')
```

While we're at it, let's update our views:

```python
# views.py

# ...

class APIBookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class APIBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

We also need to add names for our urls.

```python
# urls.py

# ...

api_urlpatterns = [
    url('^authors/$', APIBookList.as_view(), name='api_author_list'),
    url('^authors/(?P<pk>[0-9]+)/$', APIAuthorDetail.as_view(), name='api_author_detail'),
    url('^books/$', APIBookList.as_view(), name='api_book_list'),
    url('^books/(?P<pk>[0-9]+)/$', APIBookDetail.as_view(), name='api_book_detail'),
]
```

Now, if you go to http://127.0.0.1:8000/api/authors/45/ you can see that we get a list of book URLs for that author.

While we're at it, let's create a root for our API that points to our Authors and Books endpoints.

```python
# views.py

from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

# ...

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('api_author_list', request=request, format=format),
        'books': reverse('api_book_list', request=request, format=format)
    })
```

Now add the view to the `urls.py`

```python
# urls.py

# ...

from collection.views import APIAuthorList, APIAuthorDetail, APIBookList, APIBookDetail, api_root

api_urlpatterns = [
    url('^authors/$', APIBookList.as_view(), name='api_author_list'),
    url('^authors/(?P<pk>[0-9]+)/$', APIAuthorDetail.as_view(), name='api_author_detail'),
    url('^books/$', APIBookList.as_view(), name='api_book_list'),
    url('^books/(?P<pk>[0-9]+)/$', APIBookDetail.as_view(), name='api_book_detail'),
    url('^$', api_root, name='api_root')
]
```

Now check it out: http://127.0.0.1:8000/api/



### Authentication

As with forms, we don't want just anyone to be able to POST or DELETE data. We need to restrict writing to the API to authenticated users. This can be accomplishe easily by adding a permission restriction to the class based views.

```python
# views.py

from rest_framework import permissions

# ...

class APIAuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class APIAuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class APIBookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class APIBookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
```

***Note:*** `permission_classes` takes a tuple. If there is only one permission class to include, be sure to still add a comma to the end, otherwise it's not a tuple!

Now look at the resource in the browseable API, and you will see that the ability to PUT has been removed. To add login capability to the browseable API, you need to add the following to `urls.py`

```python
# urls.py

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
```

The default authentication methods used by the Django REST Framework are `SessionAuthentication` and `BasicAuthentication`, which means user id and password.

It is possible to use other forms of authentication such as using an API Key, or token: http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication

You can also use third-party authentication schemes, such as OAuth: http://www.django-rest-framework.org/api-guide/authentication/#third-party-packages

### ViewSets and Routers

Our API does pretty standard stuff. It allows you to GET lists and POST new resources to the resource list path. And it enables you to GET individual resource details and to make changes to an individual resource via PUT, POST, PATCH, and DELETE.

If we stick to that standard behavior we can reduce our work even further by using a `ViewSet` which brings all of that functionality together in a single view.

Instead of a ListView and a DetailView, we set up a single `ModelViewSet`

```python
# views.py

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIAuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class APIBookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authors': reverse('api_author_list', request=request, format=format),
        'books': reverse('api_book_list', request=request, format=format)
    })
```

Now, we need to edit out `urls.py` to work with our ViewSets. ViewSets have methods called `retrieve` and `list` and `create` instead of using the standard `get` and `post`, etc.

```python
# urls.py

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail
from collection.views import api_root, APIAuthorViewSet, APIBookViewSet

author_list = APIAuthorViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
author_detail = APIAuthorViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
book_list = APIBookViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
book_detail = APIBookViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

api_urlpatterns = [
    url('^authors/$', author_list, name='api_author_list'),
    url('^authors/(?P<pk>[0-9]+)/$', author_detail, name='api_author_detail'),
    url('^books/$', book_list, name='api_book_list'),
    url('^books/(?P<pk>[0-9]+)/$', book_detail, name='api_book_detail'),
    url('^$', api_root, name='api_root')
]

api_urlpatterns = format_suffix_patterns(api_urlpatterns, allowed=['json', 'html'])

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/', include(api_urlpatterns))    
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
```

Now test it out: http://127.0.0.1:8000/api/

OK, that worked well. The code in our `views.py` shrinked dramataically! But we ended up with more complexity in the `urls.py` file. That's where routers come in. All you do is create a `DefaultRouter`,  register your `ViewSet` with it, and include it in your `urlpatterns`. However, because the naming conventions collide with our original url pattern names, we will need to remove the names from our original patterns.

```python
# urls.py

from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail
from collection.views import api_root, APIAuthorViewSet, APIBookViewSet


router = DefaultRouter()
router.register(r'authors', APIAuthorViewSet)
router.register(r'books', APIBookViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='web_book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='web_book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='web_author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='web_author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/', include(router.urls))    
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
```

We will also need to update the `view_name` attributes in our `serializers.py` file.

```python
# serializers.py

from rest_framework import serializers
from collection.models import Book, Author


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    books = serializers.HyperlinkedRelatedField(many=True,
        queryset=Book.objects.all(), view_name='book-detail', format='html')
    url = serializers.HyperlinkedIdentityField(view_name='author-detail')

    class Meta:
        model = Author
        fields = ('url', 'id', 'last_name', 'first_name', 'birth_year', 'books')


class BookSerializer(serializers.ModelSerializer):
    author = serializers.HyperlinkedRelatedField(many=False, read_only=True,
        view_name='author-detail', format='html')
    url = serializers.HyperlinkedIdentityField(view_name='book-detail')

    class Meta:
        model = Book
        fields = ('url', 'id', 'author', 'title', 'pub_year', 'isbn', 'rating', 'notes')

```


