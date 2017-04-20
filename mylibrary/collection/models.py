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

    def __str__(self):
        return self.sortable_name


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

    def __str__(self):
        return self.title
