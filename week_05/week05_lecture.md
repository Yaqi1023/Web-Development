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


