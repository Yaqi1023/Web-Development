# Week 5 - Authentication & Authorization

Last week we learned how to build forms so that you and other users can enter data to be stored in your database. However, you probably don't want just anyone to be able to edit your data. To control who can edit data we need to do two things:

1. We need to **Authenticate** users. Authentication is the process of determining that a user is who they claim to be. There are various ways to authenticate a person: thumbprint scanners, iris scanners, and of course passwords, which we will use.

2. Once we know who a user is, we need to ensure that they can only perform the actions that we trust them to do. This is called **Authorization**. We use the concepts of groups and permissions to manage this process.

## Authentication

We will use usernames and passwords to authenticate our users. Django comes with a set of urls and views that we can use to assist in loggin our users in.

See the docs here: https://docs.djangoproject.com/en/1.11/topics/auth/


### Users

By default, the `django.contrib.auth` module is installed in your `settings.py` file. This module include the `User` model, which has the following fields:
- `username`
- `password`
- `email`
- `first_name`
- `last_name`

It also comes with an `admin` site that you can reach at http://127.0.0.1/admin

But how can you login without an existing user? You need to create your site's ***superuser*** first.

```python
$ python manage.py createsuperuser
```

This will walk you through adding username, email and address (but not first and last name for some reason).

Once you have your superuser, you can explore the `admin` site. However, that is more for authorization than authentication, so we will come to it again later.

### Login Basics

How do we login in a user in our site? Well, you could add authentication to your view by using the `login()` function, like so:

```python
# from django docs...

from django.contrib.auth import authenticate, login

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...
```

Similarly, you can log out a user with the `logout()` function...

```python
# from django docs...

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
```

You can see that we are expecting user login data from a form, which we then pass into the `auth` package's `authenticate` function. That gives us the matching `User` model. We then pass that to the `login()` function, which will add it to the Django *Session*. The Session ID is also given to the user's browser in a cookie, which will get passed with every new request. Thus, Django will know who the user is from then on.

For more info about sessions and cookies, read these:
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Sessions
- http://eli.thegreenplace.net/2011/06/24/how-django-sessions-work-introduction/

However, we do not need to implement the views above ourselves. We can use the builtin `LoginView` and `LogoutView`, which we will come to later.

Once you add login and logout functionality to your site, you can then add restrictions on certain views, to ensure that only lgged in user can access that view.

```python
# from django docs...

from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
```

As with everything else, there is a shortcut to achiveing this behavior, using a decorator:

```python
# from the django docs...

from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name='my_redirect_field')
def my_view(request):
    ...
```

Additionally, we can use User authentication data in our templates as well...

```html
<!-- from Django docs -->

{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
{% else %}
    <p>Welcome, new user. Please log in.</p>
{% endif %}

```

### Using the built-in authentication views

To add the builtin authentication views to your site, simple include the urls to your `urls.py` file, like so:

```python
# urls.py

...
urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
]
...
```

This will add the following url patterns to your site:

```
^login/$ [name='login']
^logout/$ [name='logout']
^password_change/$ [name='password_change']
^password_change/done/$ [name='password_change_done']
^password_reset/$ [name='password_reset']
^password_reset/done/$ [name='password_reset_done']
^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$ [name='password_reset_confirm']
^reset/done/$ [name='password_reset_complete']
```

However, you're not done yet. Django only gives you the url patterns and their associated views. It's up to you to provide the templates. It will look for these in a `static/registration` directory, and each template will have the same name as the url `name` with `.html` appended to it.

For example, the login view will look for a template at `static/registration/login.html` to render.

Creating the login html is not very difficult. Here is the basic pattern, which you can embellish with your own styling. The example assumes you have a `base.html` template with a `content` block which this template overrides.

```html
<!-- from the django doc -->
<!-- login.html -->

{% extends "base.html" %}

{% block content %}

{% if form.errors %}
<p>Your username and password didn't match. Please try again.</p>
{% endif %}

{% if next %}
    {% if user.is_authenticated %}
    <p>Your account doesn't have access to this page. To proceed,
    please login with an account that has access.</p>
    {% else %}
    <p>Please login to see this page.</p>
    {% endif %}
{% endif %}

<form method="post" action="{% url 'login' %}">
{% csrf_token %}
<table>
<tr>
    <td>{{ form.username.label_tag }}</td>
    <td>{{ form.username }}</td>
</tr>
<tr>
    <td>{{ form.password.label_tag }}</td>
    <td>{{ form.password }}</td>
</tr>
</table>

<input type="submit" value="login" />
<input type="hidden" name="next" value="{{ next }}" />
</form>

{# Assumes you setup the password_reset view in your URLconf #}
<p><a href="{% url 'password_reset' %}">Lost password?</a></p>

{% endblock %}
```

## Authorization

OK, now that we've seen how to authenticate a user, let's look at how to authorize them to perform changes to the data, using our `mylibrary` application.

### Via the Admin site

The easiest way to set up groups and permissions is to use the Django `admin` site.
1. Go to http://127.0.0.1:8000/admin and log in
2. Click on "Groups"
3. Click on "Add Group"
4. Enter a name for the group (e.g. "Editors")
5. In the list of permissions, select all of the permissions for books and authors and click on the right arrow.
6. Click Save

Great, we now have an Editors user group. Now let's create an Editor user to try it out.

First, create a fake Editor user:
1. Click on the "Authentication and Authorization" link in the breadcrumb.
2. Click on "Add" in the Users row.
3. Enter form information for a fake Editor and click Save.

You should now be on the detail page for the user. Here you can add permissions:
1. Give them a first and last name (optional)
2. Highlight "Editors" in the Available Groups and click the right arrow buttton.
3. Click Save

Notice that in addition to group level permissions, you can also grant a single user permissions too, Most site administrators do not like to do that as it becomes difficult to keep track.

### Via code

In addition to using the `admin` site, you can also create and assign permissions programmatically in your code. 

The following example shows how to create a permission.
```python
# From the Django docs...

from myapp.models import BlogPost
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)
```

And here we see how to grant a permission to a user in code.

```python
# from the Django docs...

myuser.groups.set([group_list])
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions.set([permission_list])
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()
```

The permissions we saw in the admin site are automatically created for each of your models. The default for each models has three permissions: `add`, `change`, `delete`. However, you can add custom permissions for your models in the model's `Meta` class, like so:

```python
# from the Django docs...

class Task(models.Model):
    ...
    class Meta:
        permissions = (
            ("view_task", "Can see available tasks"),
            ("change_task_status", "Can change the status of tasks"),
            ("close_task", "Can remove a task by setting its status as closed"),
        )
```

OK, so now we know how to create a user and grant permissions. But how do we make use of that to restrict behavior in the application?

To do that, in your views you must authenticate the `User` and then test to see if that user has permission to perform the behavior expected from that view. You use the `User` object's `has_perm()` method to test for a given permission. For example (from the Django docs...):


>Assuming you have an application with an app named `foo` and a model named `Bar`, to test for basic permissions you should use:

>- add: `user.has_perm('foo.add_bar')`
>- change: `user.has_perm('foo.change_bar')`
>- delete: `user.has_perm('foo.delete_bar')`

But once again, there is a convenient shortcut. Just add the `perm_required` deocrator to your view.

```python
# from the Django docs...

from django.contrib.auth.decorators import permission_required

@permission_required('polls.can_vote')
def my_view(request):
    ...
```

***Important Note!*** If you are using *class based views* then the normal decorators will not work because the decorator is designed to decorate a function, not a method. To use decorators with class-based views you need to use the `method_decorator` decorator.

```python
#from the Django docs...

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)
```

Additionally, you can test permissions in your templates. A logged in user's permissions will automatically be passed to the template context under the name `perms`.

```html
<!-- from the Django docs...-->
{% if perms.foo %}
    <p>You have permission to do something in the foo app.</p>
    {% if perms.foo.can_vote %}
        <p>You can vote!</p>
    {% endif %}
    {% if perms.foo.can_drive %}
        <p>You can drive!</p>
    {% endif %}
{% else %}
    <p>You don't have permission to do anything in the foo app.</p>
{% endif %}
```

## Example

OK, now that we've gone through the components of Authentication & Authorization, let's update our `mylibrary` application.

### Adding the auth urls

We simply need to "include" the auth urls in our `urls.py` file.

While we're editing the URLS, let's fix the fact that we don't have a home page. We'll simply add a homepage redirect that takes us to the books list page. We can use the `RedirectView` class directly in our `urls.py` file. No need to touch the `views.py` file at all!

```python
# urls.py

from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
]
```

### Login template

OK, now we need some login templates. Remember that we need the `registration/login.html`

First create the directory

```bash
$ mkdir collection/templates/registration
```

Now add the `login.html` file.

```html
<!-- login.html -->
{% extends 'collection/base.html' %}

{% block name %}Login{% endblock %}

{% block content %}
  <div class="container-fluid">
    <div class="row">  

      <br>

      {% if form.non_field_errors %}
        <div class="alert alert-danger alert-dismissable" role="alert">
          <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          The form data was invalid:
          {{form.non_field_errors}}
        </div>
      {% endif %}

      <div class="col-md-8 col-md-offset-2">
        <form class="form-horizontal" action="/login/" method="post">
            
          {% csrf_token %}

          <!-- Username -->
          <div class="form-group">
            <label class="col-sm-3 control-label" for="{{form.username.id_for_label}}">Username</label>
            <div class="col-sm-4">
              <input type="text" class="form-control" name="{{form.username.name}}" id="{{form.username.id}}" required>
            </div>                      
          </div>

          <!-- Password -->
          <div class="form-group">
            <label class="col-sm-3 control-label" for="{{form.password.id_for_label}}">Password</label>
            <div class="col-sm-4">
              <input type="password" class="form-control" name="{{form.password.name}}" id="{{form.password.id}}" required>
            </div>                      
          </div>

          <div class="col-sm-4 col-sm-offset-4">
            <input type="hidden" name="next" value="{% url 'home' %}" />
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>

        </form>

      </div>
    </div>
  </div>
{% endblock %}
```

### Login in the Navbar

Well, that works nicely, but it would be better to have the login as part of the top Navbar. Let's update the `base.html` file. We will also add an include for a `login_modal.html`

```html
<!-- base.html -->
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
            <ul class="nav navbar-nav pull-right">
                {% block userlinks %}
                  {% if user.is_authenticated %}
                    <li class="dropdown">
                      <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        {{user}}
                        <b class="caret"></b>
                      </a>
                      <ul class="dropdown-menu">
                        <li><a href='/logout/?next={{request.path}}'>Log out</a></li>
                        <li><a href='/password_change/?next={{request.path}}'>Change Password</a></li>
                      </ul>
                    </li>
                  {% else %}
                    <li>
                      <a href="#" data-toggle="modal" data-target="#login-form-modal">Log in</a>
                    </li>
                  {% endif %}
                {% endblock %}
              </ul>
          </div>
        </div>
      {% endblock %}

      {% block content %}
      {% endblock %}

       {% include "collection/login_modal.html" %}


    </div><!-- ./wrapper -->

    {% block script %}
      <script>
        window.drf = {
          csrfHeaderName: "{{ csrf_header_name|default:'X-CSRFToken' }}",
          csrfCookieName: "{{ csrf_cookie_name|default:'csrftoken' }}"
        };
      </script>
      <script src="{% static 'js/jquery-3.2.1.min.js' %}"></script>
      <script src="{% static 'js/bootstrap.min.js' %}"></script>
    {% endblock %}

    {% block script_extra %}
    {% endblock %}

  </body>
  {% endblock %}
</html>
```

And the modal...

```html
<!-- login_modal.html -->
          <!-- Login Form Modal -->
          <div class="modal fade" id="login-form-modal" tabindex="-1" role="dialog" aria-labelledby="Login Modal">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                
                <form class="form-horizontal" action="/login/" method="post">

                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title" id="myModalLabel">Login</h4>
                  </div>

                  <div class="modal-body"> 
                    
                    {% csrf_token %}

                    <!-- Username -->
                    <div class="form-group">
                      <label class="col-sm-3 control-label" for="username">Username</label>
                      <div class="col-sm-4">
                        <input type="text" class="form-control" name="username" id="username" required>
                      </div>                      
                    </div>

                    <!-- Password -->
                    <div class="form-group">
                      <label class="col-sm-3 control-label" for="password">Password</label>
                      <div class="col-sm-4">
                        <input type="password" class="form-control" name="password" id="password" required>
                      </div>                      
                    </div>

                  </div>

                  <div class="modal-footer">
                    <input type="hidden" name="next" value="{{request.path}}"/>
                    <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                    <button type="submit" class="btn btn-primary">Submit</button>
                  </div>

                </form>

              </div>
            </div>
          </div>
```

Now, try it out and see if you can log in from the navbar!

### Updating the views

OK, we've set up login functionality. Now let's restrict users from creating a new book or author unless they have the right permissions.

We have already created an "Editors" groups and a fake staff user. Now create a user that is not a part of the "Editors" group so we can test that it doesn't work. 

Once you have done that, update the views to restrict access to the new books and new authors forms. All you need to do is add the method decorator to the `post` methods for both books and authors.

```python
# views.py

from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
 
from collection.models import Book, Author
from collection.forms import AuthorForm, BookForm


class BookList(FormMixin, ListView):
    model = Book
    form_class = BookForm

    def get_context_data(self, **kwargs):
        context = super(BookList, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    @method_decorator(permission_required, 'collection.can_add_book')
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
```

Try creating a new book with your superuser. It should still work fine.

Now try loggin in with an untrusted user with no permissions. It should fail, but not in the way expected. It did block the creation of the user, but it also throws an error. By default, django has the login url at http://127.0.0.1:8000/accounts/login. We can change that in the settings to match the pattern we set up in our `urls.py` file.

```python
# settings.py

LOGIN_URL = '/login'
```

Now try again. It should redirect the untrusted user to log in. 

Well, that is at least blocking them. But it's also confusing. Idealy, an untrusted user should not even get the form. So let's adjust our template to dynamically load the form for trusted users only.

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
    {% if perms.collection.can_add_book %}
      <div class="col-md-12">
        <button type="button" class="btn btn-primary btn-lg pull-right" data-toggle="modal" data-target="#book-form-modal">New Book</button>

        {% include "collection/book_form_modal.html" %}
      </div>
    {% endif %}
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

Now, try logging in as both the trusted and untrusted user to see if the button and form are available.

Now do the same thing with the Authors form.















