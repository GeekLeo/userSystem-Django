from django.conf.urls import url, include
from . import views

app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^logout/', views.logout, name='logout'),
    # url(r'captcha', include('captcha.urls')),
    url(r'^confirm/$', views.register_confirm, name='confirm'),
    url(r'^changePassword/$', views.change_password, name='change_password'),
    url(r'^applyReset/$', views.apply_reset, name='apply_reset'),
    url(r'^resetPassword/$', views.reset_password, name='reset_password'),
    # url(r'^resetConfirm/$', views.reset_confirm, name='reset_confirm'),
]
