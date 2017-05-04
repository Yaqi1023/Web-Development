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

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['aria-describedby'] = 'help_block_' + key