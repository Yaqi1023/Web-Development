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
