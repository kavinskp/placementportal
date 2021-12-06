from django.conf.urls import url
from Recruiter.views import *

urlpatterns = [
    url(r'^ajax_load_edit_recruiter_form/', ajax_load_edit_recruiter_form, name='ajax_load_edit_recruiter_form'),
    url(r'^ajax_add_recruiter/(?P<company_id>[0-9]+)', ajax_add_recruiter, name='ajax_add_recruiter'),

]
