from django.conf.urls import url
from Interview.views import *

urlpatterns = [
    url(r'^manage_companies/', manage_companies, name='manage_companies'),
    url(r'^view_student_list/(?P<company_id>[0-9]+)/', view_student_list, name='view_student_list'),

    url(r'^view_company_schedule/(?P<company_id>[0-9]+)/', view_company_schedule, name='view_company_schedule'),

    url(r'^get_events/', get_events, name='get_events'),
    url(r'^view_calendar/', view_calendar, name='view_calendar'),
    url('^change_event/', change_event, name='change_event'),
    url('^ajax_load_edit_event_modal/', ajax_load_edit_event_modal, name='ajax_load_edit_event_modal'),
    url('^ajax_drag_and_save_event/', ajax_drag_and_save_event, name='ajax_drag_and_save_event'),

    url(r'^ajax_load_preference_schedule_period_form/', ajax_load_preference_schedule_period_form,
        name='ajax_load_preference_schedule_period_form'),

    url(r'^delete_preference_schedule_period/(?P<schedule_preference_id>[0-9]+)', delete_preference_schedule_period,
        name='delete_preference_schedule_period'),

    url(r'^ajax_add_schedule_preference_period/(?P<company_id>[0-9]+)/', ajax_add_schedule_preference_period,
        name='ajax_add_schedule_preference_period'),
    url('^ajax_choose_slot/', ajax_choose_slot, name='ajax_choose_slot'),
    url(r'^ajax_load_interviewer_for_slot_form/', ajax_load_interviewer_for_slot_form, name='ajax_load_interviewer_for_slot_form'),

    url(r'^approve_suggested_slot/(?P<company_slot_id>[0-9]+)/', approve_suggested_slot, name='approve_suggested_slot'),
    url(r'^reject_suggested_slot/(?P<company_slot_id>[0-9]+)/', reject_suggested_slot, name='reject_suggested_slot'),
    url(r'^delete_company_slot/(?P<company_slot_id>[0-9]+)/', delete_company_slot, name='delete_company_slot'),

    url(r'^manage_interview_rounds/(?P<company_id>[0-9]+)/', manage_interview_rounds, name='manage_interview_rounds'),

    url(r'^ajax_add_round_for_job', ajax_add_round_for_job, name='ajax_add_round_for_job'),
    url(r'^ajax_load_interview_round_form/', ajax_load_interview_round_form, name='ajax_load_interview_round_form'),

    url(r'^delete_interview_round/(?P<round_id>[0-9]+)', delete_interview_round, name='delete_interview_round'),

]
