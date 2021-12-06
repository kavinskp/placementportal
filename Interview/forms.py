from django.forms import ModelForm, TextInput
from django import forms

from Company.models import PreferenceSchedulePeriod, CompanyJob, RoundInfo, HRContactInfo, CompanyInfo
from Interview.models import Event, InterviewRound, CompanyEvent


class DateInput(forms.DateInput):
    input_type = 'date'


class CalendarEventForm(ModelForm):
    # start = forms.DateTimeField(
    #     input_formats=['%Y-%m-%dT%H:%M:%s'],
    #     widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
    # )
    # end = forms.DateTimeField(
    #     input_formats=['%Y-%m-%d %H:%M'],
    #     widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
    # )
    # start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    # end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    # start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'), required=False)
    # end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'), required=False)

    start = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, date_format='%Y-%m-%d',
                                         time_attrs={'type': 'time'}, time_format='%H:%M'))
    end = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, date_format='%Y-%m-%d',
                                                                    time_attrs={'type': 'time'}, time_format='%H:%M'))

    class Meta:
        model = Event
        fields = '__all__'
        exclude = []
        widgets = {
            'bg_color': forms.TextInput(attrs={'type': 'color', 'value': '#64B7E6'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'value': '#000000'}),
        }


class SchedulePeriodPreferenceForm(ModelForm):
    schedule_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'value': '10:00'}, ))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'value': '17:00'}))

    def clean_schedule_date(self):
        company_id = getattr(self, 'company_id', None)
        schedule_date = self.cleaned_data.get('schedule_date')
        if company_id:
            if PreferenceSchedulePeriod.objects.filter(company_id=company_id, schedule_date=schedule_date).exists():
                raise forms.ValidationError('Date Already Exists')
        return schedule_date

    def clean_end_time(self):
        start = self.cleaned_data.get('start_time')
        end = self.cleaned_data.get('end_time')
        if end < start:
            raise forms.ValidationError('End Time cannot be lesser than start time')
        return end

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company_id', None)
        super(SchedulePeriodPreferenceForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['schedule_date'].widget.attrs['readonly'] = True
        else:
            self.company_id = company_id

    class Meta:
        model = PreferenceSchedulePeriod
        fields = '__all__'
        exclude = ['company']


class InterviewRoundForm(ModelForm):
    class Meta:
        model = InterviewRound
        fields = '__all__'
        exclude = ['job', 'round_number', 'coordinator']

    def __init__(self, *args, **kwargs):
        job_id = kwargs.pop('job_id', None)
        super(InterviewRoundForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['info'].widget.attrs['disabled'] = 'True'
            self.fields['info'].required = False
        else:
            job = CompanyJob.objects.get(pk=job_id)
            self.fields['info'] = forms.ModelChoiceField(
                queryset=RoundInfo.objects.filter(company=job.company).exclude(
                    id__in=InterviewRound.objects.filter(job=job).values('info_id')))

    def clean_info(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.info
        else:
            return self.cleaned_data['info']


class ChooseRecruiterForSlotForm(ModelForm):
    class Meta:
        model = CompanyEvent
        fields = '__all__'
        exclude = ['event', 'company', 'is_scheduled', 'is_approved']

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company_id', None)
        super(ChooseRecruiterForSlotForm, self).__init__(*args, **kwargs)
        self.fields['co_ordinator'] = forms.ModelMultipleChoiceField(
            queryset=HRContactInfo.objects.filter(company_id=company_id),
        )