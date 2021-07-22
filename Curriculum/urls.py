from django.conf.urls import url
from Curriculum.views import *

urlpatterns = [
    url(r'^batches/', view_batches, name='view_batches'),
    url(r'^un_assign_hod/(?P<batch_id>[0-9]+)/', delete_batch, name='delete_batch'),
    url(r'^hods/', list_hods, name='list_hods_info'),
    url(r'^assign_hod/', assign_hod, name='assign_hod'),
    url(r'^un_assign_hod/(?P<staff_id>[0-9]+)/', un_assign_hod, name='un_assign_hod'),
    url(r'^ajax/load_faculties/', load_faculties, name='ajax_load_faculties'),
    url(r'^ajax/load_staffs/', load_staffs, name='ajax_load_staffs'),
    url(r'^view_po_details/', view_po_details, name='view_po_details'),
    url(r'^view_all_pr_details/', view_all_pr_details, name='view_all_pr_details'),
    url(r'^un_assign_po/(?P<staff_id>[0-9]+)/', un_assign_po, name='un_assign_po'),
    url(r'^assign_pr/', assign_pr, name='assign_pr'),
    url(r'^un_assign_pr/(?P<roll_no>[0-9]+)/', un_assign_pr, name='un_assign_pr'),
    url(r'^ajax/load_students_for_given_dep_batch/', load_students_for_given_dep_batch,
        name='ajax_load_students_for_given_dep_batch'),

]
