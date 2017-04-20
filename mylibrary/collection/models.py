from django.db import models


class Book(models.Model):

    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=13)
    pub_year = models.IntegerField(null=True)

    def __repr__(self):
        return '<Book: {}>'.format(self.title)
