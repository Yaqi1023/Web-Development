from rest_framework import serializers
from collection.models import Book, Author


class AuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    last_name = serializers.CharField(required=False, allow_blank=True,
        max_length=64)
    first_name = serializers.CharField(required=True, max_length=64)
    birth_year = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.birth_year = validated_data.get('birth_year', instance.birth_year)
        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'pub_year', 'isbn', 'rating', 'notes')
