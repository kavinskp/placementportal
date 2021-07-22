from django.conf.urls import url
from Accounts.views.users import *
from Accounts.views.approval import *

urlpatterns = [
    url(r'^login', login_user, name='login'),
    url(r'^signup', signup, name='signup'),
    url(r'^logout', logout, name='logout'),
    url(r'^update_profile_pre_approval', update_profile_pre_approval, name='update_profile_pre_approval'),
    url(r'^approve_users', approve_users, name='approve_users'),
]
