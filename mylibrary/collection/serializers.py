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
