# Week 3 - Django Views

This week we learn how to pass our data from the database to the web browser, by using views and templates.

But first, let's tighten up a few things with our models and database.

## 1. Model Updates

Let's flesh out our simple model from last week. Here is what we will add:
- ratings for books
- notes for books
- publication year for books
- an author (foreign key)
- an Author model with the following attributes:
  - last name
  - first name
  - year of birth

So here is our updated `models.py` file:

```python
# models.py
from django.db import models


class Author(models.Model):

    last_name = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    birth_year = models.IntegerField(null=True, blank=True)

    @property
    def sortable_name(self):
        return '{}, {}'.format(self.last_name, self.first_name)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __repr__(self):
        return '<Author: {}>'.format(self.sortable_name)


class Book(models.Model):

    RATING_CHOICES = (
        (0, 'Unrated'),
        (1, 'Hate it'),
        (2, 'Meh'),
        (3, 'Nice'),
        (4, 'Loved it'),
        (5, 'Masterpiece!')
    )

    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, null=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    pub_year = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(default=0, choices=RATING_CHOICES)
    notes = models.TextField(null=True, blank=True)

    def __repr__(self):
        return '<Book: {}>'.format(self.title)
```

***Note:*** Don't forget to create and run your migrations!

### 1.1 Choice Fields
Take note of what happened with the choice field. We use a regular `IntegerField`, though we could have used a `CharField` instead. Then we just pass in a `choices` argument. This must a be a tuple of two-item tuples. Those two-item tuples must have the stored value as the first element, and the human readable label as the second element. See the Django docs: https://docs.djangoproject.com/en/1.11/ref/models/fields/#choices

## 2. Supplied Data

Rather than creating individual records by hand in the shell, it would be nice to programatically load a set of data into our database. There are two ways we can go about doing this.
- We can create our own Django command to parse a foreign dataset and use the model classes to create new data.
- If we convert the data to the proper JSON or YAML format, we can use DJango's built in `loaddata` command.

Let's try both methods! The goal is to import a set of data from **Goodreads**. If you have an account with Goodreads, you can download a CSV file of your books (see info here: https://www.goodreads.com/help/show/5-how-do-i-import-or-export-my-books).

### 2.1 Django Commands

See the Django Commands documentation here: https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/

If you run `python manage.py` without an argument it will list all of the builtin Django commands. We have already made use of some of these, such as `startapp`, `shell`, `dbshell`, `makemigrations`, and `migrate`.

Let's create our command that parses a Goodreads CSV and creates objects from it.

You have to create a directory for your custom commands. They go in a `commands` subdirectory, which should be in a `management` subdirectory in your application, like so:

```
mylibrary/
    mylibrary/
    manage.py
    db.sqlite3
    collection/
        __init__.py
        models.py
        tests.py
        views.py
        management/
            __init__.py
            commands/
                __init__.py
                import_goodreads_data.py
```

The `__init__.py` files are important even though they are empty. That is how Python determines if a directory is a Python package or just a plain directory.

Inside our `import_goodreads_data.py` file, we will create a `Command` class, which has a `handle` method. That is where the main logic lives, though we will also create some helper methods. We will take in a single argument from the command line that tells us where to find the CSV file.

We then iterate throught the rows in the file, check to see if the author exists, and if not create one. Then create the book for that row.

Here is our final file:

```python
# import_goodreads_data.py
import csv

from django.core.management.base import BaseCommand, CommandError
from collection.models import Book, Author


STD_GR_CSV = 'collection/data/goodread_library_export.csv'


class Command(BaseCommand):

    help = "Converts Goodreads data from a CSV file and loads it"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', nargs='?', type=str, default=STD_GR_CSV)

    def handle(self, *args, **options):
        with open(options['csv_path'], 'r') as data:
            reader = csv.DictReader(data)
            for row in reader:
                try:
                    author = self.create_author(row)
                    self.create_book(row, author)
                except:
                    from pprint import pprint
                    pprint(row)

    def create_book(self, row, author):
        book = Book()
        book.author = author
        book.title = row['Title']
        book.isbn = self.get_isbn(row)
        book.pub_year = row['Year Published'] if row['Year Published'] else None
        book.rating = int(row['My Rating']) if row['My Rating']!='' else 0
        book.notes = row['My Review']
        book.save()

    def create_author(self, row):
        names = row['Author l-f'].split(',')
        lname = names[0]
        fname = ','.join(names[1:])
        try:
            author = Author.objects.get(last_name=lname, first_name=fname)
        except Author.DoesNotExist:
            author = Author(last_name=lname, first_name=fname)
            author.save()
        return author

    def get_isbn(self, row):
        isbn = None
        if row['ISBN'].strip('="') != '':
            isbn = row['ISBN13'].strip('="')
        elif row['ISBN'].strip('="') != '':
            isbn = row['ISBN'].strip('="')
        return isbn
```

**Note:** put your CSV file in the appropriate place. I put mine in a new subdirectory:
```
collection/
    data/
        goodreads_library_export.csv
```
However, since you will pass in the path on the command line, you can put it anywhere you want.

Now run your custom command ***(without the .py extension)***:

```bash
python manage.py import_goodreads_data
```

You can now go into your dbshell and check that there are indeed a bunch of rows in your database.

*Note:* You may wish to clear out your old data before doing the above. To empty your database use the following command:

```bash
python manage.py flush
```
It will ask you if you are sure you want to do that, as it is dangerous for production data, needless to say!

### 2.2 Fixtures

If we already have some data in an appropriate format we could simply load it with Django's builtin `loaddata` command. However, what does that data look like? See the documentation here: https://docs.djangoproject.com/en/1.11/howto/initial-data/

Rather than convert the Goodreads data, I chose to simply import it myself. However, sometimes it is convenient to create a JSON or YAML fixture to use for testing. The easiest way to make one is to dump out the data you already have in the database (again, not good for sensitive production data).

First lets create a `fixtures` directory:

```
collection/
    fixtures/
```

Great, now we have a place to put our dump files.

```bash
python manage.py dumpdata collection > collection/fixtures/my_goodreads.json
```

Now go open the file and see your nicely formatted JSON.

To test it out let's flush the database again and load from our fixture instead of the CSV. First rename your db and create a new one, just in case.

```bash
mv db.sqlite3 backup_db
python manage.py migrate
...
python manage.py loaddata my_goodreads
Installed 1943 object(s) from 1 fixture(s)
```

Excellent!

## 3. URLs

OK, if we are going to create a web application, our content must be addressable with URLs. So before we even get into Django views, let's discuss URL routing. See the documentation here: https://docs.djangoproject.com/en/1.11/topics/http/urls/

We havetwo models, so let's start with 4 basic pages:
- A page that lists  all books
- A page that shows a single book's details
- A page that lists all authors
- A page that shows a single author's details

To do this, we add a `url` pattern to the `urls.py` file. Let's put books and authors in their own virtual "directories", like so

```python
# urls.py

from django.conf.urls import url
from django.contrib import admin

from collection import views as collection_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/\$', collection_views.books_list, name='books_list'),
    url(r'^authors/$', collection_views.authors_list, name='authors_list')
]
```

The `url()` function takes a regex pattern as the first argument and a view function as the second argument. When Django gets an incoming request, it will compare the URL to these patterns, select the first one that matcehs and send the request on to the named view function. The `name` argument is used to reconstruct the URL pattern in other parts of the code (we'll get to that later).

So that works fine for a pretty generic page. But we don't want to create a URL pattern for every single book! How can we *dynamically* handle book details? We can use regex *groups* to pull out parts of the URL as variables. Thus, we can have object IDs in the URL, which get's passed to the view, which it uses to reqtrieve the appropriate object from the database.

Here is our complete url patterns variable:

```python
from django.conf.urls import url
from django.contrib import admin

from collection import views as collection_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', collection_views.books_list, name='books_list'),
    url(r'^books/(?P<book_id>\d+)$', collection_views.book_details, name='books_list'),
    url(r'^authors/$', collection_views.authors_list, name='authors_list'),
    url(r'^authors/(?P<author_id>\d+)$', collection_views.author_details, name='authors_list'),
]
```

OK, we now have a set of URLs to play with. Let's create the views that go with them!

## Views

Our views need to do 3 main actions:
1. process any incoming arguments
2. retrieve the appropriate set of data
3. render a response

Let's start with the books list, which doesn't deal with any incoming arguments. It just gets everything.

```
# views.py

import json
 
from django.http import HttpResponse, Http404
from django.shortcuts import render
 
from collection.models import Book, Author
 
 
def books_list(request):
    books = [str(b) for b in Book.objects.all()]
    return HttpResponse(json.dumps(books))
```

OK, we have a view. Let's test it out. Run the Django development server:

```bash
python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).
April 20, 2017 - 20:10:55
Django version 1.11, using settings 'mylibrary.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Now open http://127.0.0.1:8000/books/ in your browser. You should see something like this:

```json
[
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
"Book object",
...
]
```

### Override `__str__()` methods

Well, that's not much to look at is it? Let's override our object `__str__()` methods to get more useful information.

Add the following method to your `Book` class:

```python
# models.py

class Author(models.Model):

    ...

    def __str__(self):
        return self.sortable_name


class Book(models.Model):

    ...

    def __str__(self):
        return self.title
```

Now go to http://127.0.0.1:8000/books/ again and you should get a list of titles!

OK, now let's handle the detail page for a single book. We get the `book_id` argument from the URL dispatcher and use it to look up the correct book. We'll have to do a little extra work to make the data "printable" because the JSON decoder cannot handle values that are not integer or string literals, like `Author` foreign keys.

```python
# views.py

def book_details(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    data = {
        'title': book.title,
        'author': book.author.full_name,
        'pub_year': book.pub_year,
        'isbn': book.isbn,
        'rating': book.rating,
        'notes': book.notes,
        'id': book.id
    }
    return HttpResponse(json.dumps(data))
```

Now go to http://127.0.0.1:8000/books/12 to see a list of the book attributes. Be sure to test an ID number that actually exists. Then try one that definitely does not exist to see how Django's `Http404` error will automatically deliver an error page for you.

OK, now let's do the same for authors:

```python
def authors_list(request):
    authors = [str(a) for a in Author.objects.all()]
    return HttpResponse(json.dumps(authors))
 
 
def author_details(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    return HttpResponse(json.dumps(str(author)))
```

Great, that works. But it's not very pretty is it? Instead of delivering raw JSON, wouldn't it be nice if we could return HTML? But just like with the URL patterns, we don't want to create an HTML file for every object. Instead, it would be better to create a *template* for an object page, and the we could just plug in a specific objects data in the appropriate places.

## Templates

Learn how Views "render" templates: https://docs.djangoproject.com/en/1.11/intro/tutorial03/. Pay attention to the namespacing issue. Thus we should put our templates in a nested directory like so:

```
collection/
    templates/
        collection/
            books_list.html
            book_details.html
            authors_list.html
            author_details.html
```

Study the Django template syntax: https://docs.djangoproject.com/en/1.11/topics/templates/#the-django-template-language

Now, let's reconfigure our views to use the templates instead of JSON. Let's start with the books list.

```python
# views.py

def books_list(request):
    books = Book.objects.order_by('-rating')
    return render(request, 'collection/books_list.html', {'books': books})
```

OK, now let's create a simple HTML template:

```html
<!-- books_list.html -->
<html>
  <body>
    <h1>My books</h1>
    <table>
      <tr>
        <th>Title</th>
        <th>Author</th>
        <th>Published</th>
        <th>Rating</th>
      </tr>
      {% for book in books %}
      <tr>
        <td><a href="/books/{{book.id}}">{{book.title}}</a></td>
        <td>{{book.author.full_name}}</td>
        <td>{{book.pub_year}}</td>
        <td>{{book.rating}}</td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
```

Now check out http://127.0.0.1:8000/books and see our response. It's now in HTML (though still ugly).

Let's go ahead and take care of all the other views and templates.

```python
# views.py

import json
 
from django.http import HttpResponse, Http404
from django.shortcuts import render
 
from collection.models import Book, Author
 
 
def books_list(request):
    books = Book.objects.order_by('-rating')
    return render(request, 'collection/books_list.html', {'books': books})
 
 
def book_details(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    return render(request, 'collection/book_details.html', {'book': book})
 
def authors_list(request):
    authors = Author.objects.order_by('last_name', 'first_name')
    return render(request, 'collection/authors_list.html', {'authors': authors})
 
 
def author_details(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
        books = author.book_set.all()
    except Author.DoesNotExist:
        raise Http404("Author does not exist")
    return render(request, 'collection/author_details.html', {'author': author, 'books': books})
```



```html
<!-- book_details.html -->

<html>
<body>
  <h1>{{book.title}}</h1>
  <h2>Details</h2>
  <ul>
    <b>Author: </b>{{book.author.full_name}}<br/>
    <b>Published: </b>{{book.pub_year}}<br/>
    <b>ISBN: </b>{{book.isbn}}<br/>
  </ul>
  <h2>My Review</h2>
  <ul>
    <b>Rating: </b>{{book.rating}}<br/>
    <b>Notes: </b>{{book.notes}}<br/>
  </ul>
</body>
</html>
```

```html
<!-- authors_list.html -->
<html>
  <body>
    <h1>Authors</h1>
    <table>
      <tr>
        <th>Last Name</th>
        <th>First Name</th>
        <th>Birth year</th>
      </tr>
      {% for author in authors %}
      <tr>
        <td><a href="/authors/{{author.id}}">{{author.last_name}}</a></td>
        <td><a href="/authors/{{author.id}}">{{author.first_name}}</a></td>
        <td>{{author.birth_year}}</td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
```

```html
<!-- author_details.html -->

<html>
  <body>
    <h1>{{author.full_name}}</h1>
    <h2>Books</h2>
    <table>
      <tr>
        <th>Title</th>
        <th>Author</th>
        <th>Published</th>
        <th>Rating</th>
      </tr>
      {% for book in books %}
      <tr>
        <td><a href="/books/{{book.id}}">{{book.title}}</a></td>
        <td>{{book.pub_year}}</td>
        <td>{{book.rating}}</td>
      </tr>
      {% endfor %}
    </table>
  </body>
</html>
```

Great we now have pages for all our resources with hyperlinks between list pages and item detail pages.

But it's till ugly! How can we make it pretty? Well you could study CSS and create your own style. But if you are like me and want to leave design up to designers, and juts want a simple solution for works in progress, then you should use a CSS framework. There are many to choose from:
- [Twitter Bootstrap](http://getbootstrap.com/)
- [Zurb Foundation](http://foundation.zurb.com/)
- [Material Design]()
- [Bulma](http://bulma.io/)
- [Pure](https://purecss.io/)
- [Skeleton](http://getskeleton.com/)
- and many more

For our demonstration we will be using Bootstrap. Please download it. You will also need to download [jQuery](https://jquery.com/download/) and put the files in your app directory like so:

```bash
collection/
  static/
    js/
      bootstrap.js
      bootstrap.min.js
      jquery-3.2.1.min.js
    css/
      bootstrap.css
      bootstrap.css.map
      bootstrap.min.css
      bootstrap.min.css.map
      bootstrap-theme.css
      bootstrap-theme.css.map
      bootstrap-theme.min.css
      bootstrap-theme.min.css.map
    fonts/
      glyphicons-halflings-regular.eot
      glyphicons-halflings-regular.svg
      glyphicons-halflings-regular.ttf
      glyphicons-halflings-regular.woff
      glyphicons-halflings-regular.woff2
```

Now we need to let Django know where to put our static files.  Edit the `settings.py` file

```python
# settings.py

...
STATIC_ROOT = 'static'
```

Now run the `collectstatic` command. When you do this, Django will look at all of your apps (we only have one so far) collect all of their static files, and put them in a single place. This is useful if you want your static files served differently than your Python executables.

```bash
python manage.py collectstatic
```

OK, now that we have Bootstrap installed, let's start by creating a `base.html` template that has our boilerplate html. Then our other templates will *extend* it by filling in the main body.

```html
<!--- base.html -->

{% load staticfiles %}

<!DOCTYPE html>
<html>
  <head>
    {% block head %}

      {% block meta %}
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <meta name="robots" content="NONE,NOARCHIVE" />
      {% endblock %}

      <title>{% block title %}{% block name %}{% endblock %} - GRI Digital Services{% endblock %}</title>

      {% block style %}
        <link rel="stylesheet" type="text/css" href="{% static 'css/bootstrap.min.css' %}" />
      {% endblock %}

      {% block style_extra %}
      {% endblock %}


    {% endblock %}
  </head>

  {% block body %}
  <body class="{% block bodyclass %}{% endblock %}">

    <div class="wrapper">
      {% block navbar %}
        <div class="navbar navbar-static-top {% block bootstrap_navbar_variant %}navbar-inverse{% endblock %}">
          <div class="container">
            <span>
              {% block branding %}
                <a class='navbar-brand' rel="nofollow" href='/'>
                    My Library
                </a>
              {% endblock %}
            </span>
            <ul class="nav navbar-nav">
              <li class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">List Views<span class="caret"></span></a>
                <ul class="dropdown-menu">
                  <li><a href="/books/">Books List</a></li>
                  <li><a href="/authors/">Authors List</a></li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      {% endblock %}

      {% block content %}
      {% endblock %}


    </div><!-- ./wrapper -->

    {% block script %}
      <script src="{% static 'js/jquery-3.2.1.min.js' %}"></script>
      <script src="{% static 'js/bootstrap.min.js' %}"></script>
    {% endblock %}

    {% block script_extra %}
    {% endblock %}

  </body>
  {% endblock %}
</html>
```

```html
<!-- books_list.html -->
{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <h1>My books</h1>
  <table class="table">
    <tr>
      <th>Title</th>
      <th>Author</th>
      <th>Published</th>
      <th>Rating</th>
    </tr>
    {% for book in books %}
    <tr>
      <td><a href="/books/{{book.id}}">{{book.title}}</a></td>
      <td><a href="/authors/{{book.author.id}}">{{book.author.full_name}}</a></td>
      <td>{{book.pub_year}}</td>
      <td>{{book.rating}}</td>
    </tr>
    {% endfor %}
  </table>
</div>
{% endblock %}
```

```html
<!-- book_details.html -->
{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>{{book.title}}</h1>
    <h2>Details</h2>
    <dl>
      <dt>Author</dt><dd><a href="/authors/{{book.author.id}}">{{book.author.full_name}}</a></dd>
      <dt>Published</dt><dd>{{book.pub_year}}</dd>
      <dt>ISBN</dt><dd>{{book.isbn}}</dd>
    </dl>
    <h2>My Review</h2>
    <dl>
      <dt>Rating</dt><dd>{{book.rating}}</dd>
      <dt>Notes</dt><dd>{{book.notes}}</dd>
    </ul>
  </div>
</div>
{% endblock %}
```

```html
<!-- authors_list.html -->

{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>Authors</h1>
  </div>
  <table class="table">
    <tr>
      <th>Last Name</th>
      <th>First Name</th>
      <th>Birth year</th>
    </tr>
    {% for author in authors %}
    <tr>
      <td><a href="/authors/{{author.id}}">{{author.last_name}}</a></td>
      <td><a href="/authors/{{author.id}}">{{author.first_name}}</a></td>
      <td>{{author.birth_year}}</td>
    </tr>
    {% endfor %}
  </table>
</div>
{% endblock %}
```

```html
<!-- author_details.html -->

{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>{{author.full_name}}</h1>
  </div>
  <h2>Books</h2>
  <table class="table">
    <tr>
      <th>Title</th>
      <th>Author</th>
      <th>Published</th>
      <th>Rating</th>
    </tr>
    {% for book in books %}
    <tr>
      <td><a href="/books/{{book.id}}">{{book.title}}</a></td>
      <td>{{book.pub_year}}</td>
      <td>{{book.rating}}</td>
    </tr>
    {% endfor %}
  </table>
</div>
{% endblock %}
```