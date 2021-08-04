from django.conf.urls import url
from Accounts.views.users import *
from Accounts.views.approval import *

urlpatterns = [
    url(r'^login', login_user, name='login'),
    url(r'^signup', signup, name='signup'),
    url(r'^activate/(?P<key>.+)/', activation, name='activation'),
    url(r'^new-activation-link/(?P<user_id>\d+)$', new_activation_link, name='new_activation_link'),
    url(r'^logout', logout, name='logout'),
    url(r'^view_profile', view_profile, name='view_profile'),
    url(r'^update_profile_pre_approval', update_profile_pre_approval, name='update_profile_pre_approval'),
    url(r'^approve_staffs', approve_staff_accounts, name='approve_staffs'),
    url(r'^approve_students', approve_student_accounts, name='approve_students'),
    url(r'^approve_interviewers', approve_interviewer_accounts, name='approve_interviewers'),

    url(r'^ajax_get_user_profile_json', ajax_get_user_profile_json, name='ajax_get_user_profile_json')
]
