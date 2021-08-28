from django.forms import ModelForm
from django import forms
from Curriculum.models import Batch, Regulation
from Accounts.views.utils import getActiveDepartments, getActiveRegulation


class BatchForm(ModelForm):
    regulation = forms.ModelChoiceField(
        queryset=getActiveRegulation(),
        widget=forms.Select(attrs={'class': 'form-select'}))
    department = forms.ModelChoiceField(
        queryset=getActiveDepartments(),
        widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Batch
        fields = '__all__'
        exclude = ['active', 'interview_allowed']


class RegulationForm(ModelForm):

    def save(self, commit=True):
        obj = super(RegulationForm, self).save(commit=False)
        if obj.end_year is None:
            if obj.programme_period is not None and obj.programme_period > 0:
                obj.end_year = obj.start_year + obj.programme_period
                self.save()

    class Meta:
        model = Regulation
        fields = '__all__'
        exclude = ['active']


class UpdateRegulationForm(ModelForm):
    start_year = forms.IntegerField(disabled=True)
    end_year = forms.IntegerField(disabled=True)
    programme = forms.CharField(disabled=True)

    def clean_current_semester(self):
        current_sem = self.cleaned_data.get('current_semester')
        if current_sem > 0:
            programme = self.cleaned_data.get('programme')
            start_year = self.cleaned_data.get('start_year')
            programme_period = self.cleaned_data.get('programme_period')
            if current_sem > programme_period * 2:
                raise forms.ValidationError(
                    'Cannot be greater than ' + str(programme_period * 2) + " for this regulation!")
            reg_objs = Regulation.objects.filter(programme=programme, current_semester=current_sem).exclude(
                start_year=start_year)
            if reg_objs.exists():
                raise forms.ValidationError(
                    'Another regulation started in different year in this programme has same value!')
        return 0

    def save(self, commit=True):
        obj = super(UpdateRegulationForm, self).save(commit=False)
        if obj.end_year is None:
            if obj.programme_period is not None and obj.programme_period > 0:
                obj.end_year = obj.start_year + obj.programme_period
                self.save()

    class Meta:
        model = Regulation
        fields = ['start_year', 'end_year', 'current_semester']
