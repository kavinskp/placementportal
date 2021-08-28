from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^company$', company_index, name='company_index'),
    url(r'^dashboard/', dashboard, name='dashboard'),
    # url(r'^logout', logout, name='logout'),
    # url(r'^profile', profile, name='profile'),
]
