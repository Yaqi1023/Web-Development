from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail, author_list, author_detail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/authors/$', author_list),
    url('^api/authors/(?P<pk>[0-9]+)/$', author_detail)
]
