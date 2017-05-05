# Week 4 - Views, continued

## Class-based Views

So far, the views we created were functions. But we can also create Python classes with methods that implement our views. This enables us to use inheritance and mixins, and thus improve the strcuture of our code and reduce duplication of effort.

All class-based views inherit from the base `View` class. Django comes with a set of generic class-based views that you can use out of the box. These include: `TemplateView`, `RedirectView`, `ListView`, `DetailView`, `FormView` and more. You can see a list of them here: https://docs.djangoproject.com/en/1.11/ref/class-based-views/


The most obvious advantage of class-based views is responding to different HTTP methods for the same resources.

### A review of HTTP Methods

Recall the methods of the HyperText Transfer Protocol:
- `GET` Retrieves the specified resource(s). You can pass parameters in the query string to refine the request. 
    - Example: `http://www.example.com/books?year=2017`
- `POST` Sends data to the specified URL. Often used to create a new resource of a certainn type. 
    - For example, you would likely post a new books information to `http://www.example.com/books/` and a new authors information to `http://www.example.com/authors/`
- `PUT` Creates or overwrites a resource at the specified URL. 
    - For example, if we already had a book at `http://www.example.com/books/1bh342bh5`, then sending book data in a `PUT` request would overwrite the existing book data.
- `PATCH` Similar to `PUT`, but this allows you to only send the new pieces of data, whereas `PUT` is a complete overwrite.
- `DELETE` Delets the item at the specified URL.
- `HEAD` Retrieves the HTTP header metadata, but not the resource data. 
    - This can include useful information such as the last time the data was updated. For large resources, this can be useful to avoid unneccessary downloads of already cached data.

There are a few other, somewhat obscure HTTP methods. See here for more details: 
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods
- https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol

---

A Django class-based view allows you to define a method to respond to each of these types of requests instead of creating conditional branches in a  single function.

Here is an example function based view that responds to both `GET` and `PUT` requests (adapted from Django Docs example):

```python
# views.py

from django.http import HttpResponse

def my_view(request):
    if request.method == 'GET':
        # retrieve data and perform other logic
        return HttpResponse('result')
    if request.method == 'PUT':
        # validate and save new data
        return HttpResponse('result')
```

In a class-based view, this would become:

```python
from django.http import HttpResponse
from django.views import View

class MyView(View):
    def get(self, request):
        # retrieve data and perform other logic
        return HttpResponse('result')

    def put(self, request):
        # validate and save new data
        return HttpResponse('result')
```

In the `urls.py` file you pass the your view in, but you must call the `as_view()` method, since the `url()` function expects a callable function.

```python
# urls.py
from django.conf.urls import url
from myapp.views import MyView

urlpatterns = [
    url(r'^some/path/pattern/$', MyView.as_view()),
]
```

### Built-in Generic Class-based Views

OK, let's try adapting our `mylibrary` app to use class-based views.

First let's use the `ListView` to generate our list views of books and authors.

```python
from django.view.generic import ListView
 
from collection.models import Book, Author


class BookList(ListView):
    model = Book


class AuthorList(ListView):
    model = Author
```

Great, but we need to update two more things:
1. The `ListView` adds a variable named `object_list` to the template context. We need to update the templates to look for that variable instead of the one we were previously passing to the context.
    - In `books_list.html` change `{% for book in books %}` to `{% for book in object_list %}`
    - In `authors_list.html` change `{% for author in authors %}` to `{% for author in object_list %}`
2. We also need tp update our `urls.py` file to use the new class view instead of our functions.
    ```python
    # urls.py
    from django.conf.urls import url
    from django.contrib import admin

    from collection.views import BookList, AuthorList, book_details, author_details


    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^books/$', BookList.as_view(), name='books_list'),
        url(r'^books/(?P<book_id>\d+)$', book_details, name='books_list'),
        url(r'^authors/$', AuthorList.as_view(), name='authors_list'),
        url(r'^authors/(?P<author_id>\d+)$', author_details, name='authors_list'),
    ]
    ```

The `ListView` class expects to find a template with a name `<model_name>_list.html`. However, ours uses plurals `books_list.html` so we need to rename them.

```bash
$ mv books_list.html book_list.html
$ mv authors_list.html author_list.html
```

Great! Now test it out with `python manage.py runserver` and go to http://127.0.0.1:8000/books/ and http://127.0.0.1:8000/authors/

OK, now let's do the same with our item detail views. We will use the `DetailView` class.

First, we update our `views.py`

```python
# views.py
from django.views.generic import ListView, DetailView
 
from collection.models import Book, Author


class BookList(ListView):
    model = Book


class AuthorList(ListView):
    model = Author


class BookDetail(DetailView):
    model = Book
 

class AuthorDetail(DetailView):
    model = Author
```

Look how much simpler our code has become!

OK, now we need to rename our templates again.

```bash
$ mv book_details.html book_detail.html
$ mv author_details.html author_detail.html
```

Finally, we update our `urls.py` file.

```python
# urls.py
from django.conf.urls import url
from django.contrib import admin

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='books_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='authors_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
]
```

OK, now let's try it out with `python manage.py runserver`
- go to http://127.0.0.1:8000/books/1
- go to http://127.0.0.1:8000/authors/1

***Uh oh!*** The book details page looks fine, but the authors detail page is missing the list of books by that author.

We need to override the context generated by the `DetailView` class.

```python
# views.py
# ...

class AuthorDetail(DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        context['books'] = self.object.book_set.all()
        return context
```

Now go to http://127.0.0.1:8000/authors/1. Voila! It works!

One more things. Let's make it so that the authors list is in alphabetical order. To do this we add a `Meta` class to our model.

```python
# models.py
# ...

class Author(models.Model):

    last_name = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    birth_year = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

#   ...
```

## Forms

OK, we've got some nice views of our data. But how do we add to the data?

For that, we need forms for user input! Which means we need forms!

Django forms intro: https://docs.djangoproject.com/en/1.11/topics/forms/

***HTML Form Basics:***
- HTML can have a `<form>` element.
- Inside that, it can have `<input>` elements.
- `<input>` elements can be text boxes, check boxes, date pickers, dropdowns, etc.
- They also usually have a label attached to them.
- Some inputs can be hidden. These are used to pass data to the form handler without the user knowing.
    - For example, you may want to dynamically tell the handler what page should be rendered after the input has been processed.
- The form should also have an input with a `type` attribute of `submit`.
    - This is usually the button that tells the browser to send the data.
- The `<form>` element must also have two attributes:
    - `action` tells the browser where to send the input data. It is the URL of your form handler
    - `method` refers to the HTTP method. This is almost always `POST` but it can be `GET` as well.

Here is an example of an HTML form.
```html
<form action="/login/" method="post">
    <label for="userid">User ID: </label>
    <input id="userid" type="text" name="userid" value="{{ userid }}">
    <label for="pswd">Password: </label>
    <input id="pswd" type="password" name="pswd">
    <input type="submit" value="Login">
</form>
```

A lot of work is involved in handling forms. But Django can do a lot of that work for you. At a high level, it can:
- retrieve data to be edited in the form and prepare it
- create all or parts of the HTML form for you
- receive, validate, and save incoming data

***Django Form Basics***

See https://docs.djangoproject.com/en/1.11/topics/forms/#building-a-form-in-django

1. **The Form class:** To start using forms, we need to create a form class in a `forms.py` file. These classes look a lot like Django models, with fields of different types.
2. **The view:** Next we need to get an instance of the form in our view and add it to the context
3. **The templae:** Finally, we put the form elements into a template. We can do this manually or let Django do it all for us.

Some other things to be aware of:
- Bound vs unbound forms: https://docs.djangoproject.com/en/1.11/topics/forms/#bound-and-unbound-form-instances
- Widgets: https://docs.djangoproject.com/en/1.11/topics/forms/#widgets
- Cleaned Data: https://docs.djangoproject.com/en/1.11/topics/forms/#field-data
- Form rendering options: https://docs.djangoproject.com/en/1.11/topics/forms/#form-rendering-options
- Manually rendering forms: https://docs.djangoproject.com/en/1.11/topics/forms/#rendering-fields-manually
- Error messages: https://docs.djangoproject.com/en/1.11/topics/forms/#rendering-form-error-messages

So, let's try building a form for our authors.

We start with the `forms.py` file

```python
# forms.py

from django import forms


class AuthorForm(forms.Form):

    last_name = forms.CharField(label='Last Name', max_length=64)
    first_name = forms.CharField(label='First Name', max_length=64)
    birth_year = forms.IntegerField(label='Birth Year')
```

OK, now let's update our AuthorList view. We will make use of `FormMixin` with our `ListView` class. See the docs: https://docs.djangoproject.com/en/1.10/topics/class-based-views/mixins/

```python
# views.py

from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
 
from collection.models import Book, Author
from collection.forms import AuthorForm

# ...

class AuthorList(FormMixin, ListView):
    model = Author
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super(AuthorList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        #self.object = self.get_object()
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
```

And now let's update our template with a form modal.

```html
<!-- author_list.html -->
{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>Authors</h1>
  </div>
  <div class="row">
    <div class="col-md-12">
      <button type="button" class="btn btn-primary btn-lg pull-right" data-toggle="modal" data-target="#author-form-modal">New Author</button>

      {% include "collection/author_form_modal.html" %}
    </div>
  </div>
  <div class="row">
    <br>
    <table class="table">
      <tr>
        <th>Last Name</th>
        <th>First Name</th>
        <th>Birth year</th>
      </tr>
      {% for author in object_list %}
      <tr>
        <td><a href="/authors/{{author.id}}">{{author.last_name}}</a></td>
        <td><a href="/authors/{{author.id}}">{{author.first_name}}</a></td>
        <td>{{author.birth_year}}</td>
      </tr>
      {% endfor %}
    </table>
  </div>
</div>
{% endblock %}
```

And our new include for the modal

```html
<!-- author_form_modal.html -->
        <!-- Author Form Modal -->
        <div class="modal fade" id="author-form-modal" tabindex="-1" role="dialog" aria-labelledby="Author Form Modal">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <form class="form" action="/authors/" method="post">

                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                  <h4 class="modal-title" id="myModalLabel">Author Form</h4>
                </div>

                <div class="modal-body">
                  {% csrf_token %}
                  {{ form }}
                  <input type="submit" value="Submit" />
                </div>
              </form>
            </div>
          </div>
        </div>
```

Now go to http://127.0.0.1:8000/authors/ and try adding yourself as an author!

OK, let's add a form for Books. But let's make use of the ModelForm instead of the basic form.

See the docs: https://docs.djangoproject.com/en/1.10/topics/forms/modelforms/

Our new `forms.py` file

```python
# forms.py

from django import forms
from django.forms import Form, ModelForm

from collection.models import Book


class AuthorForm(Form):

    last_name = forms.CharField(label='Last Name', max_length=64)
    first_name = forms.CharField(label='First Name', max_length=64)
    birth_year = forms.IntegerField(label='Birth Year')


class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

```

Our `views.py`

```python
# views.py

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

# ...
```

And our templates

```html
<!-- book_list.html -->

{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>My Books</h1>
  </div>
  <div class="row">
    <div class="col-md-12">
      <button type="button" class="btn btn-primary btn-lg pull-right" data-toggle="modal" data-target="#book-form-modal">New Book</button>

      {% include "collection/book_form_modal.html" %}
    </div>
  </div>
  <div class="row">
    <br>
    <table class="table">
      <tr>
        <th>Title</th>
        <th>Author</th>
        <th>Published</th>
        <th>Rating</th>
      </tr>
      {% for book in object_list %}
      <tr>
        <td><a href="/books/{{book.id}}">{{book.title}}</a></td>
        <td><a href="/authors/{{book.author.id}}">{{book.author.full_name}}</a></td>
        <td>{{book.pub_year}}</td>
        <td>{{book.rating}}</td>
      </tr>
      {% endfor %}
    </table>
  </div>
</div>
{% endblock %}
```

```html
<!-- book_form_modal.html -->

        <!-- Book Form Modal -->
        <div class="modal fade" id="book-form-modal" tabindex="-1" role="dialog" aria-labelledby="Book Form Modal">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <form class="form" action="/books/" method="post">

                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                  <h4 class="modal-title" id="myModalLabel">Book Form</h4>
                </div>

                <div class="modal-body">
                  {% csrf_token %}
                  {{ form }}
                  <input type="submit" value="Submit" />
                </div>
              </form>
            </div>
          </div>
        </div>
```

So, our forms works, but it looks ugly. That's because the default `widgets` that Django uses don't include the CSS classes we need for Boostrap to style them correctly. So let's fix them.

But first, let's fix the look of our Book detail page...

```html
<!-- book_detail.html -->

{% extends 'collection/base.html' %}

{% load staticfiles %}

{% block name %}Books List{% endblock %}

{% block content %}
<div class="container">
  <div class="jumbotron">
    <h1>{{book.title}}</h1>
  </div>
  <div class="row">
    
    <div class="col-md-6">
      <div class="panel panel-default">
        <div class="panel-heading">Details</div>
        <div class="panel-body">
          <dl class="dl-horizontal">
            <dt>Author</dt>
            <dd><a href="/authors/{{book.author.id}}">{{book.author.full_name}}</a></dd>
        
            <dt>Published</dt>
            <dd>{{book.pub_year}}</dd>
        
            <dt>ISBN</dt>
            <dd>{{book.isbn}}</dd>
          </dl>
        </div>
      </div>
    </div>

    <div class="col-md-6">
      <div class="panel panel-default">
        <div class="panel-heading">My Review</div>
        <div class="panel-body">
          <dl class="dl-horizontal">
            
            <dt>Rating</dt>
            <dd>{{book.rating}}</dd>
            
            <dt>Notes</dt>
            <dd>{{book.notes}}</dd>
          </dl>
        </div>
      </div>
    </div>
    
  </div>
</div>
{% endblock %}
```

OK, we need to update the widget for each field in our form:

```python
# forms.py

class BookForm(ModelForm):

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-describedby'] = 'help_block_' + key
```

Now, let's update out book form modal

```html
<!-- book_form_modal.html -->

        <!-- Book Form Modal -->
        <div class="modal fade" id="book-form-modal" tabindex="-1" role="dialog" aria-labelledby="Book Form Modal">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <form class="form-horizontal" action="/books/" method="post">

                <div class="modal-header">
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                  <h4 class="modal-title" id="myModalLabel">Book Form</h4>
                </div>

                <div class="modal-body">
                  {% csrf_token %}

                  {% for input in form %}

                  <div class="form-group {% if form_method == "post" and input.errors %}has-error{% endif %}">
                      <label class="col-sm-3 control-label" for="{{input.id_for_label}}">{{ input.label }}</label>
                      <div class="col-sm-4">
                        {{ input }}
                        {% if form_method == "post" and input.errors %}
                          {% for error in input.errors %}
                        <span id="help_block_{{input.name}}" class="help-block">{{error}}</span>
                          {% endfor %}
                        {% endif %}
                      </div>                      
                    </div>

                  {% endfor %}
                </div>

                <div class="modal-footer">
                  <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                  <button type="submit" class="btn btn-primary">Save</button>
                </div>
                
              </form>
            </div>
          </div>
        </div>
```