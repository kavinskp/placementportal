from django.conf.urls import url
from Interview.views import *

urlpatterns = [
    url(r'^filter_students_for_company/(?P<company_id>[0-9]+)/', filter_students_for_company,
        name='filter_students_for_company'),
    url(r'^view_company_details/(?P<company_id>[0-9]+)/', view_company_details, name='view_company_details'),
    url(r'^manage_companies/', manage_companies, name='manage_companies'),
    url(r'^view_student_list/(?P<company_id>[0-9]+)/', view_student_list, name='view_student_list'),

]
