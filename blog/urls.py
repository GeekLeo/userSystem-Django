from django.conf.urls import url, include
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/', views.create, name='create'),
    url(r'^detail/(?P<blog_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^comment/', views.comment, name='comment'),

]
