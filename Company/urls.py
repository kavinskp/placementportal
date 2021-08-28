from django.conf.urls import url
from Company.views import *

urlpatterns = [
    url(r'^register_company', register_company, name='register_company'),
    url(r'^add_hr/(?P<company_id>[0-9]+)', add_hr_info, name='add_hr_info'),
    url(r'^add_job_info/(?P<company_id>[0-9]+)', create_roles, name='create_roles'),
    url(r'^add_role/(?P<company_id>[0-9]+)', create_roles, name='add_role'),

    url(r'^add_criteria_for_job/(?P<company_id>[0-9]+)', create_roles, name='create_roles'),
    url(r'^delete_recruiter/(?P<company_id>[0-9]+)/(?P<recruiter_id>[0-9]+)', delete_recruiter,
        name='delete_recruiter'),

    url(r'^edit_criteria/(?P<company_id>[0-9]+)/(?P<criteria_id>[0-9]+)', edit_criteria, name='edit_criteria'),
    url(r'^delete_criteria/(?P<company_id>[0-9]+)/(?P<criteria_id>[0-9]+)', delete_criteria, name='delete_criteria'),
    url(r'^update_role/(?P<company_id>[0-9]+)/(?P<role_id>[0-9]+)', update_role, name='edit_role'),
    url(r'^delete_role/(?P<company_id>[0-9]+)/(?P<role_id>[0-9]+)', delete_role, name='delete_role'),
    url(r'^preview_role_document/(?P<role_id>[0-9]+)', preview_role_document, name='preview_role_document'),

    url(r'^ajax_get_criteria_for_company', ajax_get_criteria_for_company, name='ajax_get_criteria_for_company'),
    url(r'^ajax_load_company_details', ajax_load_company_details, name='ajax_load_company_details'),
    url(r'^ajax_get_allowed_batches_for_job', ajax_get_allowed_batches_for_job,
        name='ajax_get_allowed_batches_for_job'),
]
