from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'captcha', include('captcha.urls')),
    url(r'^confirm/$', views.user_confirm, name='confirm'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^apply_reset/$', views.apply_reset, name='apply_reset'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^reset_confirm/$', views.reset_confirm, name='reset_confirm'),
]
