# Week 7 - Front-end Development

So far, almost all of our development has been server-side code. Django handles our business logic and renders our templates into HTML documents before delivering a response. We added the Bootstrap CSS framework to style our pages. This also required adding some JavaScript files. We included the jQuery package as well as Bootstrap's own package. However, we did not look deeply at how these packages work. We simply followed the examples in the Bootstrap documentation. 

This week we will take a closer look at client-side code. JavaScript is the only language supported across all browsers, so we will look at some of it's fundamental properties and how it can be used to manipulate web pages. Next we will look at the jQuery package, which adds some highly useful features that abstract away a lot of commonly used boilerplate code. Finally, we will take a look at the growing world of JavaScript web frameworks. These are complex packages intended for full web development, just like Django. They follow the MVC framework just like Django. However, they do not talk directly to a database. Instead, they use server-side APIs, like we buit last lecture to retrieve and manipulate data. 

## 1. JavaScript

OK, let's go over the basics of JavaScript. Open up your browser, go to the developer tools and open the console. This will give you an interactive interpreter to work with.

### 1.1 Statements, Variables, and Values

A lot of the syntax is similar. Try executing a few math operations. Most of them work just fine. However, there are few key differences in the syntax.

- `//`: The `//` operator does not do the same thing as Python. In Python, it performs integer division without the remainder or decimal. In JavaScript it is a **comment**. 

- **statements & code blocks**: Python statements are terminated by line ends, and code blocks are denoted by indentation. In JavaScript, statements are terminated by semicolons `;`. Some statements do not require this, but some do. To be safe, just use them for every statement. Code blocks are marked by curly braces `{ }`. This means that white space and indentation do not matter. However, you should attempt to keep your code readable by using white space consistently. *The convention in JavaScript is to use 2 spaces for indentation, as opposed to four spaces in Python.* This is good because JavaScript statements tend to be longer than Python.

- `Infinity` and `NaN`: In Python, if you divide by zero you get an error. In JavaScript, the interpreter tries very hard to not "crash", so instead it returns values.
    - `1/0` -> `Infinity`
    - `-1/0` -> `-Infinity`
    - `0/0` -> `NaN` which means "Not a Number"

- `true` & `false`: not capitalized, unlike Python.

- *falsy values*: The following values are falsy:
    - `false`
    - `0`
    - `NaN`
    - `""` *empty string*
    - `null` *a deliberate non-value, as opposed to something that is undefined*
    - `undefined` - for instance the result of a function with no return value

- *Equality*: In JavaScript there are two ways to test for equality.
    - `==` - Double equals will coerce data types before conducting the comparison
        - Thus, `"42" == 42;` is `true`
    - `===` - Triple equals tests for actual equality.
        - Thus, `"42" === 42` is `false`

- To **var**, or not to **var**
    - Use `var` to declare a variable: `var x = 11;`
    - If you do not use `var`, the variable will have global scope `y = 33;`
        - Don't do that!
            - *Except when you really mean to.*

- *Incrementing & Decrementing*
    - Just like Python, you can quickly increment a value using `+=`
        - `x += 5;`
    - Additionally, like **C** and **Java** you can increment by 1 using `++`.
        - `x++;`
    - The same works for decrementing, with `--`
        - `x--;`

### 1.2 Data Structures

- *Arrays*: In JavaScript arrays work similar to Python lists.
    - `var stuff = ['popcorn', 33, false];`
    - Instead of `append`, use `push` to add values to the end.
        - `stuff.push('junk');`
    - Instead of `len()`, use the array's `length` method
        - `stuff.length();`

- *Objects*: A JavaScript *object* is the same as a Python *dictionary*
    - You don't have to use quotes for the key as long as it doesn't have white space or other special characters
        - var book = {title: "1984", author: "Orwell, George"};
    - You can access the values using the "subscript" syntax like Python:
        - book['title'];
    - However, you can also use dot notation:
        - book.author;

### 1.3 Control Structures

Control structures like `if` and `while` work similar to Python. The key differences include:
- There is no `elif`. Use `else if` instead
- ***Don't forget to use curly braces!***
        
```javascript

if (x === 0) {
    // due something
} else if (x === 1) {
    // do something else
} else {
    // third option
}

while (x > 0) {
    // do something
}
```

JavaScript also has a `do .. while` loop. This ensures that the loop runs at least once!

```js
do {
    // do something
} while (x < 0)
```

JavaScript has two kinds of `for` loops. The traditional kind, like **C** programming:

```js
for (z = 1; z < 10; z++) {
    console.log(z);
}
```

This kind of a loop requires three pieces of information:
1. The initial state: `z = 1;`
2. The test to perform before each iteration: `z < 10;`
3. The action to perform at the close of each iteration: `z++`

It also has a `for ... in` loop, which is closer to Python

```js
for (var k in stuff) {
    // do something
}
```

JavaScript also supports the `switch` control structure, which Python does not.

```js
var auto_type = 'truck';

switch(auto_type) {
    case 'car':
        // do car stuff
        break;
    case 'truck':
        // do truck stuff
        break;
    case 'van':
        // do van stuff
        break;
    case 'bus':
        // do bus stuff
        break;
    default:
        // do generic stuff
        break;
}
```

### 1.4 Functions

Instead of `def`, use `function` when defining a function.

```js
function max(numbers) {
  var high = -Infinity;
  for (var num in numbers) {
    if (num > high) {
      high = num;
    }
  }
  return high;
}
```

***Anonymous functions:*** You can pass functions around like other variable values, just like in Python. You can also define a function anonymously in the parameter list for another function.

```js
function myFunction(someArray, someFunc) {
    return someFunc(someArray);
}

var numbers = [1,2,3,4,5,6];

myFunction(numbers, function(vals) {
    // do something 
    }
);
```

### 1.4 Prototypes

JavaScript is not a pure Object-Oriented programming language. It is a **Prototype** language. This means that it does not instantiate concrete objects from abstract classes. Instead, new objects can be created from others, or from basic functions. They can inherit properties from their *prototypes* rather than from parent classes.

As we saw, an object in JavaScript is simply a dictionary. But you can assign functions to them. And you can access other attributes of the object inside the function using `this`.

```js
var person = {
    lastName: "Vonnegut",
    firstName: "Kurt",
    fullName: function() { return this.firstName + " " + this.lastName; }
}
person.fullName();
```
However, `this` refers to the context in which the function was called, which may differ from the context in which it was defined.

```js
var genericFullName = person.fullName;
genericFullName(); // Error
```

Conversely, we could first define a function which uses `this`, then attache it to an object, and `this` will then refer to the object!

```js
var lastFirst = function() {
    return this.lastName + ", " + this.firstName;
}

person.lastFirst = lastFirst;
person.lastFirst();
```

You can create a constructor and call it using the `new` keyword. Using `new` will tell JavaScript to create a new object when calling the function.

```js
var Square = function(side) {
    this.side = side;
    this.area = function() {return this.side * this.side;}
}

var sq1 = new Square(3);
sq1.area();
```

JavaScript objects inherit from their ***prototypes*** instead of from a parent class. You can usually access (and change) the prototype via the `__proto__` attribute. However, this is not supported in all browsers.

```js
sq1.__proto__ = {perimeter: function(){return this.side * 4;}}

sq1.perimeter();
```

## The DOM

OK, so you've got some of the basics of JavaScript. You have enough knowledge to write a program. But how do you manipulate a web page with it? That's where the **Document Object Model (DOM)** comes in. The DOM is an object-roeinted representation of an HTML document. The objects making up this model are accessible through a standard API delivered by the browser (though each browser tweaks the standard in some ways).

The most commonly used objects in the API are `window` which represents the browser itself, `document` which is the root node of the HTML document, and `Element` which is used for most HTML elements, though it can be subclassed for different types of elements like a form or table.

Let's try interacting with the DOM via JavaScript. Create an HTML document with the following markup, open it in your browser, and go to the developer console.

```html
<html>
    <head>
        <title>Basic Page for Testing</title>
    </head>
    <body>
        <div id="div1">
            <p class="first-sentences">Here is a paragraph</p>
            <p>Here is a second paragraph</p>
        </div>
        <div id="div2">
            <p class="first-sentences">This paragraph is in a separate div element</p>
            <p>This on is too</p>
        </div>
    </body>
</html>
```

OK, you should see a page with just four lines of text. Let's try manipulating it with code in the console.

Let's try grabbing a single element by it's ID.

```js
d1 = document.getElementById('div1');
d1.style.color = "red";

d1.align = "right";
```

OK, now let's try grabbing a set of similar elements.

```js
alldivs = document.getElementsByTagName('div');

for (var i=0; i<alldivs.length; i++) {
    alldivs[i].style.border = "thick solid black";
}
```

Finally, let's try grabbing a set of elements by their class name.

```js
firsts = document.getElementsByClassName('first-sentences');

for (var i=0; i<firsts.length; i++) {
    var p = firsts[i];
    var text = p.textContent;
    p.innerHTML = "<h1>" + text + "</h1>";
}

```

For a thorough introduction to the DOM and it's API, you should consult the Mozilla Developer Network website: https://developer.mozilla.org/en-US/docs/Web/API

I do not intend to go any further into raw JavaScript. Lots of tools have been developed over the past decade that make front end development much easier. The king of such tools is the jQuery package.

## jQuery

Manipulating the DOM is great, but the code to do it can be a bit tedious. In 2006, jQuery was introduced as an easier way to access and manipulate the DOM elements. Let's take a look.

Edit your basic HTML file to include the jQuery package...

```html
<html>
    <head>
        <title>Basic Page for Testing</title>
        <script
            src="https://code.jquery.com/jquery-3.2.1.min.js"
            integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
            crossorigin="anonymous"></script>
    </head>
    <body>
        <div id="div1">
            <p class="first-sentences">Here is a paragraph</p>
            <p class="second-sentences">Here is a second paragraph</p>
        </div>
        <br/>
        <div id="div2">
            <p class="first-sentences">This paragraph is in a separate div element</p>
            <p class="second-sentences">This on is too</p>
        </div>
        <br/>
        <div >
            <button id="toggler" href="#">Some button</button>
        </div>
    </body>
</html>
```

Now, open it up and go to the console again.

```js
$('#div1').hide();

$('#div1').show();

$('.first-sentences').css('color', 'red');

$('div').css('border', 'thick solid blue');
```

That  was much easier wasn't it? But jQuery offers a lot more than just easy lookup and manipulation of elements. It also offers easier handling of events and making Ajax calls, which required a lot of boilerplate code in the old days.

```js
$('#toggler').click(function(event){
    $('.first-sentences').toggle();
});
```

Cool. So what are the kinds of events that we can react to? See the docs here: http://api.jquery.com/category/events/

Create another version of the test html and put it in the static files section of your `mylibrary` project's `collection` application: `mylibrary/collection/static/html/test.html`

```html
<html>
    <head>
        <title>Basic Page for Testing</title>
        <script
            src="https://code.jquery.com/jquery-3.2.1.min.js"
            integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4="
            crossorigin="anonymous"></script>
    </head>
    <body>
        <div id="div1">
            <p class="first-sentences">Here is a paragraph</p>
            <p class="second-sentences">Here is a second paragraph</p>
        </div>
        <br/>
        <div id="div2">
            <p class="first-sentences">This paragraph is in a separate div element</p>
            <p class="second-sentences">This on is too</p>
        </div>
        <br/>
        <div >
            <button id="toggler" href="#">Toggle!</button>
        </div>
        <div>
            <input id="bookid" type="text">
            <button id="fetcher" href="#">Fetch Book</button>
            <div id="book-data"></div>
        </div>
    </body>
    <script>
        $('#toggler').click(function(event){
            $('.first-sentences').toggle();
        });

        $('#fetcher').on('click', function(event) {
            var bookid = $('#bookid').val();
            $.ajax({
                url: 'http://127.0.0.1:8000/api/books/'+bookid+'.json',
                success: function(result) {
                    console.log(result);
                    var html = '';
                    $.each(result, function(key, value) {
                        html += key + ": " + value + "<br/>"
                    });
                    $('#book-data').html(html);
                },
                error: function(jqxhr, textStatus, errorThrown) {
                    console.log('ERROR: ' + textStatus + '\n' + errorThrown);
                }
            });
        });
    </script>
</html>
```

Now open the file in your browser at http://127.0.0.1:8000/static/html/test.html to your ajax at work.

Great. Now how could we make use of that in our current system? Recall that we developed forms to create new authors and new books. What if we wanted to delete a book? Well, unfortunately, browsers only support the GET and POST HTTP methods. We cannot just create an hTML form with `method="DELETE"`. However, all HTTP methods can be executed via AJAX, and this is where jQuery can help us out. Let's add a "Delete" button to our book detail page.

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
  <div class="row">
  {% if perms.collection.can_delete_book %}
    {% include "collection/book-delete-modal.html" %}
      <div class="col-md-12">
        <button type="button" class="btn btn-danger btn-lg pull-right" data-toggle="modal" data-target="#book-delete-modal">Delete Book</button>
      </div>
  {% endif %}
  </div>
</div>
{% endblock %}

{% block script_extra %}
<script>
    $('#delete').submit(function(e) {
      e.preventDefault();
      $.ajaxSetup({
        beforeSend: function(xhr, settings) {
          if(!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
          }
        }
      });
      $.ajax({
        type: 'DELETE',
        url: '/books/{{book.id}}',
        success: function() {
          window.location.href = '/books/'
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
          console.log(errorThrown);
          console.log(textStatus);
          window.location.href = '/login/'
        }
      });
    });
  </script>
{% endblock %}
```

OK, now let's add the DELETE modal template

```html
<!-- book-delete-modal.html -->
          <div class="modal fade" id="book-delete-modal" tabindex="-1" role="dialog" aria-labelledby="Book Delete Modal">
            <div class="modal-dialog" role="document">
              <div class="modal-content">
                
                <form id="delete" class="form-horizontal" action="" method="post">
                    {% csrf_token %}

                    <div class="modal-header">
                      <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                      <h4 class="modal-title" id="myModalLabel">Delete Book {{book.id}}</h4>
                    </div>

                    <div class="col-md-offset-1">
                      <span class="text-danger">Are you sure you wish to delete this book?</span>
                    </div>

                    <div class="modal-footer">
                      <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>

                      <input type="submit" class="btn btn-danger" value="Delete" />
                    </div>
                </form>
              </div>
            </div>
          </div>
```

OK, now we need to update our views

```python
# views.py

# ...
class BookDetail(DetailView):
    model = Book

    @method_decorator(permission_required('collection.delete_book'))
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        request.session['deleted_book'] = '"{}" ({})'.format(book.title, book.id)
        book.delete()
        return JsonResponse({})

# ...

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
```

Let's also update the Book List template to display our message about the deleted item

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
  {% if deleted_book %}
    <div class="alert alert-success alert-dismissible" role="alert">
      <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      Book {{deleted_book}} deleted
    </div>

...
```

There is a lot to explore with jQuery. More than can be fit into a single lecture. So go explore the documentation on your own.

## MV* Frameworks

Finally, we come to front end frameworks. These work similarly to server-side frameworks like Django or Ruby on Rails. However, instead of models mapping and talking to a database, the models map to a server side API. We already have a fully compliant server side API built using the Django REST Framework. That means we could build a completely decoupled user interface using just JavaScript. Let's take a look at some of these frameworks.

You can find a good comparison of them at http://todomvc.com