import datetime
import json

from django import forms
from django.contrib.auth.decorators import permission_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib import messages
from django.urls import reverse

from Accounts.models import StudentAccount, UserPermissions, UserGroups
from Company.models import CompanyJob, CompanyInfo, HRContactInfo, RoundInfo, PreferenceSchedulePeriod
from Company.forms import HRContactInfoForm, RoundInfoForm
from Interview.forms import CalendarEventForm, SchedulePeriodPreferenceForm, InterviewRoundForm, ChooseRecruiterForSlotForm
from Interview.models import StudentInterviewEnroll, CompanyInterview, Event, CompanyEvent, InterviewRound


def is_po(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_OFFICER.group_name()).exists():
        return True
    return False


def is_pr(user):
    if user.groups.filter(name=UserGroups.PLACEMENT_REPRESENTATIVE.group_name()).exists():
        return True
    return False


def get_company_list(user):
    company_list = None
    if is_po(user):
        company_list = CompanyInfo.objects.filter().distinct()
    elif is_pr(user):
        student_obj = StudentAccount.objects.get(user=user)
        company_list = CompanyInfo.objects.filter(companyjob__criteria__batch=student_obj.info.batch).distinct()
    return company_list


# Create your views here.
@permission_required(UserPermissions.CAN_APPROVE_INTERVIEWER.get_permission())
def manage_companies(request):
    company_list = get_company_list(request.user).distinct()
    return render(request, 'manage_companies.html', {
        'company_list': company_list
    })


def view_company_details(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    return render(request, 'view_company_info.html', {
        'company': company_info
    })


def view_student_list(request, company_id):
    company_obj = CompanyInfo.objects.get(pk=company_id)
    jobs = []
    for job in company_obj.companyjob_set.all():
        job_dict = {}
        job_dict.update({'id': job.id})
        job_dict.update({'name': job.role_name})
        student_data_filled = False
        try:
            company_interview = CompanyInterview.objects.get(company_id=company_id)
            if company_interview.marked_for_enroll:
                job_dict.update({'marked_for_enroll': company_interview.marked_for_enroll})
                job_dict.update({'status': company_interview.get_status_display()})
                interested_students = StudentInterviewEnroll.objects.filter(job=job, applied__gt=0)
                not_interested_students = StudentInterviewEnroll.objects.filter(job=job, applied__lt=0)
                undecided_students = StudentInterviewEnroll.objects.filter(job=job, applied=0)
                job_dict.update({'interested_students': interested_students})
                job_dict.update({'not_interested_students': not_interested_students})
                job_dict.update({'undecided_students': undecided_students})
                student_data_filled = True
        except CompanyInterview.DoesNotExist:
            pass
        if not student_data_filled:
            job_dict.update({'eligible_students': get_students_matching_criteria(job.criteria)})
        jobs.append(job_dict)
    context = {'jobs': jobs, 'company': company_obj}
    return render(request, 'view_student_list.html', context)


def get_company(company_info):
    try:
        return CompanyInterview.objects.get(company=company_info)
    except CompanyInterview.DoesNotExist:
        return CompanyInterview.objects.create(company=company_info)


def ajax_add_schedule_preference_period(request, company_id):
    error = None
    if request.method == 'POST':
        form = SchedulePeriodPreferenceForm(request.POST, company_id=company_id)
        try:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.company = CompanyInfo.objects.get(pk=company_id)
                instance.save()
                msg = "Saved Preferred Range " + str(instance) + " !"
                messages.success(request, msg)
            else:
                if form.errors:
                    error = {}
                    for err in form.errors:
                        error_ms = []
                        for er in form.errors.get(err):
                            error_ms.append(er)
                        error.update({err: str.join(' ', error_ms)})
        except forms.ValidationError as e:
            error = [str(e)]
    if error:
        response = HttpResponse(
            json.dumps(error),
            content_type='application/javascript; charset=utf8'
        )
        response.status_code = 403
        return response
    else:
        response = HttpResponse("success")
        response.status_code = 200
        return response


def view_company_schedule(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    company = get_company(company_info)
    error = None
    events = None
    slotDate = None
    if request.method == 'POST':
        if 'schedule_interview' in request.POST:
            date = request.POST['slotDate']
            isAllDay = request.POST.get('isAllDay', '') == 'on'
            if not isAllDay:
                start_time = request.POST['startTime']
                end_time = request.POST['endTime']
                start = datetime.datetime.strptime(date + " " + start_time, '%Y-%m-%d %H:%M')
                end = datetime.datetime.strptime(date + " " + end_time, '%Y-%m-%d %H:%M')
                start = start.replace(tzinfo=datetime.timezone.utc)
                end = end.replace(tzinfo=datetime.timezone.utc)
            else:
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
                next_date = date + datetime.timedelta(days=1)
                start = date.replace(tzinfo=datetime.timezone.utc)
                end = next_date.replace(tzinfo=datetime.timezone.utc)
            event = Event.objects.create(name=request.POST['eventName'],
                                         allday=isAllDay,
                                         start=start,
                                         end=end)
            CompanyEvent.objects.create(company_id=company_id,
                                        event=event)
            pass
        if 'add_schedule_preference_period' in request.POST:
            form = SchedulePeriodPreferenceForm(request.POST, company_id=company_id)
            try:
                if form.is_valid():
                    instance = form.save(commit=False)
                    company_id = request.POST['id']
                    instance.company = CompanyInfo.objects.get(pk=company_id)
                    instance.save()
                    msg = "Saved Preferred Range " + str(instance) + " !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if form.errors:
                        error = []
                        for err in form.errors:
                            for er in form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        elif 'edit_schedule_preference_period' in request.POST:
            id = request.POST['id']
            entry = get_object_or_404(PreferenceSchedulePeriod, pk=id)
            form = SchedulePeriodPreferenceForm(request.POST, instance=entry, company_id=company_id)
            try:
                if form.is_valid():
                    instance = form.save()
                    msg = "Saved Preferred Range " + str(instance) + " !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if form.errors is not None:
                        error = []
                        for err in form.errors:
                            for er in form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        elif 'edit_recruiter_for_scheduled_slot' in request.POST:
            id = request.POST['id']
            entry = get_object_or_404(CompanyEvent, pk=id)
            form = ChooseRecruiterForSlotForm(request.POST, instance=entry, company_id=company_id)
            try:
                if form.is_valid():
                    instance = form.save()
                    msg = "Recuriters changed for slot " + str(instance) + " !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if form.errors is not None:
                        error = []
                        for err in form.errors:
                            for er in form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
    else:
        if 'slotDate' in request.GET:
            slotDate = request.GET.get('slotDate', None)
            date = datetime.datetime.strptime(slotDate, '%Y-%m-%d')
            next_date = date + datetime.timedelta(days=1)
            start = date.replace(tzinfo=datetime.timezone.utc)
            end = next_date.replace(tzinfo=datetime.timezone.utc)
            events = Event.objects.filter(start__lte=start, end__gt=start).union(
                Event.objects.filter(start__lt=end, end__gt=end)).union(
                Event.objects.filter(start__gte=start, end__lt=end))

    form = SchedulePeriodPreferenceForm(company_id=company_id)
    return render(request, 'view_company_schedule.html',
                  {'company': company, 'company_info': company_info, 'form': form, 'slotDate': slotDate,
                   'eventsInDate': events,
                   'error_msg': error})


def approve_suggested_slot(request, company_slot_id):
    instance = CompanyEvent.objects.get(pk=company_slot_id)
    instance.is_scheduled = True
    instance.is_approved = 1
    instance.save()
    msg = "Approved suggested schedule" + str(instance) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('view_company_schedule', instance.company_id)


def reject_suggested_slot(request, company_slot_id):
    instance = CompanyEvent.objects.get(pk=company_slot_id)
    instance.is_approved = -1
    if instance.is_scheduled:
        instance.is_approved = 0
        instance.is_scheduled = False
    instance.save()
    msg = "Rejected suggested schedule " + str(instance) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('view_company_schedule', instance.company_id)


def delete_company_slot(request, company_slot_id):
    instance = CompanyEvent.objects.get(pk=company_slot_id)
    instance.delete()
    instance.event.delete()
    msg = "Deleted company event " + str(instance) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('view_company_schedule', instance.company_id)


def get_students_matching_criteria(criteria):
    min_cgpa = criteria.min_cgpa if criteria.min_cgpa is not None else 0.0
    max_cgpa = criteria.max_cgpa if criteria.max_cgpa is not None else 10.0
    x_min_per = criteria.min_x_percentage if criteria.min_x_percentage is not None else 0.0
    x_max_per = criteria.max_x_percentage if criteria.max_x_percentage is not None else 100.0
    x11_min_per = criteria.min_x11_percentage if criteria.min_x11_percentage is not None else 0.0
    x11_max_per = criteria.max_x11_percentage if criteria.max_x11_percentage is not None else 100.0
    students = StudentAccount.objects.filter(info__batch__in=criteria.get_allowed_batches(),
                                             info__cgpa__gte=min_cgpa,
                                             info__cgpa__lte=max_cgpa,
                                             info__x_percentage__gte=x_min_per,
                                             info__x_percentage__lte=x_max_per,
                                             info__x11_percentage__gte=x11_min_per,
                                             info__x11_percentage__lte=x11_max_per
                                             )
    if criteria.history is not None:
        students = students.filter(info__history_of_backlogs__lte=criteria.history)
    if criteria.current is not None:
        students = students.filter(info__current_backlogs__lte=criteria.current)
    return students


def view_calendar(request):
    form = CalendarEventForm()
    context = {
        'form': form
    }
    return render(request, 'view_calendar.html', context)


def get_events(request):
    print(request.GET)
    if 'start' in request.GET and 'end' in request.GET:
        all_events = Event.objects.filter(start__gte=request.GET['start'],
                                          end__lte=request.GET['end'])
    else:
        all_events = Event.objects.all()
    events = []
    for event in all_events:
        if event.start is not None and event.end is not None:
            events.append({
                'title': event.name,
                'id': event.id,
                'start': event.start,
                'end': event.end,
                # 'start': datetime.datetime.strptime((str(event.start.date()) + "T" + str(event.start.time())),
                #                                     "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M"),
                # 'end': datetime.datetime.strptime((str(event.end.date()) + "T" + str(event.end.time())),
                #                                   "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M"),
                'backgroundColor': event.bg_color,
                'textColor': event.text_color,
                'description': event.description,
                'allDay': event.allday
            })
    return JsonResponse(events, safe=False)


def change_event(request):
    if request.method == 'POST':
        if 'add_event' in request.POST:
            form = CalendarEventForm(request.POST)
            print(request.POST)
            if form.is_valid():
                event_instance = form.save()
                msg = "Event - " + str(event_instance.name) + " is added !"
                messages.success(request, msg)
            else:
                if form.errors:
                    error = []
                    for err in form.errors:
                        for er in form.errors.get(err):
                            error.append(er)
        elif 'edit_event' in request.POST:
            event_id = request.POST['id']
            event_instance = Event.objects.get(pk=event_id)
            event = CalendarEventForm(request.POST, instance=event_instance)
            event.save()
            msg = "Event - " + str(event_instance.name) + " is saved !"
            messages.success(request, msg)
        elif 'delete_event' in request.POST:
            event_id = request.POST['id']
            event_instance = Event.objects.get(pk=event_id)
            event_instance.delete()
            msg = "Event - " + str(event_instance.name) + " is deleted !"
            messages.success(request, msg)
    return redirect('view_calendar')


def ajax_drag_and_save_event(request):
    error = None
    msg = None
    try:
        print(request.GET)
        event_id = request.GET['id']
        event_instance = Event.objects.get(pk=event_id)
        event_instance.start = request.GET['start']
        event_instance.end = request.GET['end']
        event_instance.save()
        msg = "Event - " + str(event_instance.name) + " is saved !"
    except Exception as e:
        error = [str(e)]
    if error:
        messages.error(request, error)
        response = HttpResponse(
            json.dumps(error),
            content_type='application/javascript; charset=utf8'
        )
        response.status_code = 403
        return response
    else:
        response = HttpResponse(msg)
        response.status_code = 200
        return response


def ajax_load_edit_event_modal(request):
    event_id = request.GET['event_id']
    entry = get_object_or_404(Event, pk=event_id)
    form = CalendarEventForm(instance=entry)
    otherLinks = []
    return render(request, 'ajax_load_form_in_div.html', {
        'form': form,
        'action_url': reverse('change_event'),
        'submit_name': 'edit_event',
        'delete_btn': 'Delete Event',
        'delete_name': 'delete_event',
        'id': event_id,
        'otherLinks': otherLinks
    })


def ajax_load_preference_schedule_period_form(request):
    schedule_preference_id = request.GET.get('schedule_preference_id', None)
    if schedule_preference_id is None:
        company_id = request.GET.get('company_id')
        form = SchedulePeriodPreferenceForm(company_id=company_id)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/ajax_add_schedule_preference_period/' + company_id + "/",
        })
    else:
        entry = get_object_or_404(PreferenceSchedulePeriod, pk=schedule_preference_id)
        form = SchedulePeriodPreferenceForm(instance=entry)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/view_company_schedule/' + str(entry.company_id) + "/",
            'submit_name': 'edit_schedule_preference_period',
            'id': schedule_preference_id
        })


def delete_preference_schedule_period(request, schedule_preference_id):
    instance = PreferenceSchedulePeriod.objects.get(pk=schedule_preference_id)
    instance.delete()
    msg = "Removed preferred range " + str(instance) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('view_company_schedule', instance.company_id)


def ajax_choose_slot(request):
    if request.method == 'GET':
        slotDate = request.GET.get('slotDate', None)
        date = datetime.datetime.strptime(slotDate, '%Y-%m-%d')
        next_date = date + datetime.timedelta(days=1)
        start = date.replace(tzinfo=datetime.timezone.utc)
        end = next_date.replace(tzinfo=datetime.timezone.utc)
        events = Event.objects.filter(start__lte=start, end__gt=start).union(
            Event.objects.filter(start__lt=end, end__gt=end)).union(
            Event.objects.filter(start__gte=start, end__lt=end))
        serialized_obj = serializers.serialize('json', events)
        response = HttpResponse(serialized_obj)
        response.status_code = 200
        return response
    if request.method == 'POST':
        print(request.POST)

    error = None
    if error:
        response = HttpResponse(
            json.dumps(error),
            content_type='application/javascript; charset=utf8'
        )
        response.status_code = 403
        return response
    else:
        response = HttpResponse("success")
        response.status_code = 200
        return response


def manage_interview_rounds(request, company_id):
    company_info = CompanyInfo.objects.get(pk=company_id)
    company = get_company(company_info)
    error = None
    if request.method == 'POST':
        if 'add_interview_round' in request.POST:
            job_id = request.POST['id']
            form = InterviewRoundForm(request.POST, job_id=job_id)
            try:
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.job = CompanyJob.objects.get(pk=job_id)
                    instance.save()
                    form.save_m2m()
                    msg = "Added Round for job " + str(instance.job) + " !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if form.errors:
                        error = []
                        for err in form.errors:
                            for er in form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
        if 'edit_interview_round' in request.POST:
            round_id = request.POST['id']
            instance = InterviewRound.objects.get(pk=round_id)
            form = InterviewRoundForm(request.POST, instance=instance)
            try:
                if form.is_valid():
                    instance = form.save()
                    msg = "Changed Round Details " + str(instance) + " !"
                    messages.success(request, msg)
                else:
                    error = ["Please Enter correct Details!!"]
                    if form.errors:
                        error = []
                        for err in form.errors:
                            for er in form.errors.get(err):
                                error.append(er)
            except forms.ValidationError as e:
                error = [str(e)]
    return render(request, 'manage_interview_rounds.html',
                  {'company': company, 'company_info': company_info, 'error_msg': error})


def ajax_add_round_for_job(request):
    error = None
    if request.method == 'POST':
        job_id = request.POST['job_id']
        form = InterviewRoundForm(request.POST, job_id=job_id)
        try:
            if form.is_valid():
                instance = form.save(commit=False)
                instance.job = CompanyJob.objects.get(pk=job_id)
                instance.round_number = 0
                instance.save()
                msg = "Added Round for job " + str(instance.job) + " !"
                messages.success(request, msg)
            else:
                if form.errors:
                    error = {}
                    for err in form.errors:
                        error_ms = []
                        for er in form.errors.get(err):
                            error_ms.append(er)
                        error.update({err: str.join(' ', error_ms)})
        except forms.ValidationError as e:
            error = [str(e)]
    if error:
        response = HttpResponse(
            json.dumps(error),
            content_type='application/javascript; charset=utf8'
        )
        response.status_code = 403
        return response
    else:
        response = HttpResponse("success")
        response.status_code = 200
        return response


def delete_interview_round(request, round_id):
    instance = InterviewRound.objects.get(pk=round_id)
    instance.delete()
    msg = "Removed round " + str(instance) + " !"
    messages.success(request, msg)
    if request.GET.get('next') is not None:
        return redirect(request.GET.get('next'))
    return redirect('manage_interview_rounds', instance.company_id)


def ajax_load_interview_round_form(request):
    round_id = request.GET.get('round_id', None)
    if round_id is None:
        job_id = request.GET.get('job_id')
        company_id = request.GET.get('company_id')
        form = InterviewRoundForm(job_id=job_id)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/manage_interview_rounds/' + company_id + "/",
            'submit_name': 'add_interview_round',
            'id': job_id
        })
    else:
        entry = get_object_or_404(InterviewRound, pk=round_id)
        form = InterviewRoundForm(instance=entry, job_id=entry.job_id)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/manage_interview_rounds/' + str(entry.job.company_id) + "/",
            'submit_name': 'edit_interview_round',
            'id': round_id
        })


def ajax_load_interviewer_for_slot_form(request):
    slot_id = request.GET.get('slot_id', None)
    if slot_id is not None:
        slot_id = request.GET.get('slot_id')
        com_event = CompanyEvent.objects.get(pk=slot_id)
        form = ChooseRecruiterForSlotForm(company_id=com_event.company_id, instance=com_event)
        return render(request, 'ajax_load_form_in_div.html', {
            'form': form,
            'action_url': '/view_company_schedule/' + str(com_event.company_id) + "/",
            'submit_name': 'edit_recruiter_for_scheduled_slot',
            'id': slot_id
        })