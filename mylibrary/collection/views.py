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
 