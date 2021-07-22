from django.conf.urls import url
from Company.views import *
from PlacementPortal import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^crf/', crf, name='create_company'),
    url(r'^register_company', register_company, name='register_company'),
    url(r'^add_hr/(?P<company_id>[0-9]+)', add_hr_info, name='add_hr_info'),
    # url(r'^company_info/(?P<company_id>[0-9]+)/', edit_company_info, name='edit_company_info'),
]