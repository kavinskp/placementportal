from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login', login_user, name='login'),
    url(r'^signup', signup, name='signup'),
    url(r'^logout', logout, name='logout'),
    url(r'^profile', profile, name='profile'),
]
