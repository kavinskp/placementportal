from django.forms import ModelForm
from django import forms
from dal import autocomplete
from Curriculum.models import Batch, Department, Regulation
from Accounts.views.utils import getActiveDepartments


class BatchForm(ModelForm):
    department = forms.ModelChoiceField(
        queryset=getActiveDepartments(),
        widget=autocomplete.ModelSelect2())

    def clean_department(self):
        department = self.cleaned_data.get('department')
        regulation = self.cleaned_data.get('regulation')
        if Batch.objects.filter(regulation=regulation, department=department).exists():
            raise forms.ValidationError('Batch Already exists for same regulation and department.')
        return department

    def clean_current_semester(self):
        current_sem = self.cleaned_data.get('current_semester')
        if current_sem > 0:
            regulation = self.cleaned_data.get('regulation')
            period = regulation.programme_period
            if current_sem > period * 2:
                raise forms.ValidationError('Cannot be greater than ' + str(period * 2) + " for this regulation!")
            batch_obj = Batch.objects.filter(regulation=regulation)
            if batch_obj.exists():
                batch_obj = batch_obj[0]
                if batch_obj.current_semester != current_sem:
                    raise forms.ValidationError('Same regulation batch has different value.')
            else:
                same_prog_objs = Batch.objects.filter(regulation__programme=regulation.programme)
                if same_prog_objs.exists():
                    if same_prog_objs.filter(current_semester=current_sem).exists():
                        raise forms.ValidationError(
                            'Another ' + str(regulation.programme) + ' programme has same current semester value!')
            return current_sem
        return 0

    class Meta:
        model = Batch
        fields = '__all__'
        exclude = ['in_active']
