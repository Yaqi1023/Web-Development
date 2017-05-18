from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import RedirectView

from rest_framework.routers import DefaultRouter

from collection.views import BookList, AuthorList, BookDetail, AuthorDetail
from collection.views import APIAuthorViewSet, APIBookViewSet


router = DefaultRouter()
router.register(r'authors', APIAuthorViewSet)
router.register(r'books', APIBookViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$', BookList.as_view(), name='book_list'),
    url(r'^books/(?P<pk>\d+)$', BookDetail.as_view(), name='book_detail'),
    url(r'^authors/$', AuthorList.as_view(), name='author_list'),
    url(r'^authors/(?P<pk>\d+)$', AuthorDetail.as_view(), name='author_detail'),
    url(r'^$', RedirectView.as_view(url='/books/'), name='home'),
    url('^', include('django.contrib.auth.urls')),
    url('^api/', include(router.urls))    
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

