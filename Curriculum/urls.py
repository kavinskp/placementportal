from django.conf.urls import url
from Curriculum.views import *

urlpatterns = [
    url(r'^batches/', view_batches, name='view_batches'),
    url(r'^regulations/', view_regulations, name='view_regulations'),
    # url(r'^update_batch/(?P<batch_id>[0-9]+)/', update_batch, name='update_batch'),
    # url(r'^delete_batch/(?P<batch_id>[0-9]+)/', mark_as_active_batch, name='mark_as_active_batch'),
    url(r'^mark_as_active_batch/(?P<batch_id>[0-9]+)/', mark_as_active_batch, name='mark_as_active_batch'),
    url(r'^delete_regulation/(?P<regulation_id>[0-9]+)/', delete_regulation, name='delete_regulation'),
    url(r'^delete_batch/(?P<batch_id>[0-9]+)/', delete_batch, name='delete_batch'),
    url(r'^hods/', view_hods, name='view_hods'),
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
    url(r'^ajax_load_regulation_form', ajax_load_regulation_form, name='ajax_load_regulation_form'),

]
