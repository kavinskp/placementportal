from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect

from Company.models import CompanyInfo, HRContactInfo, Criteria, CompanyJob
from Accounts.views.utils import getInterviewAllowedBatches
import re


class CompanyInfoForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Short Name'}))
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Full Name'}))
    type = forms.ChoiceField(
        choices=CompanyInfo.TYPES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    website = forms.URLField(max_length=200,
                             initial="https://",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Home Page URL'}))

    class Meta:
        model = CompanyInfo
        fields = ['name', 'full_name', 'website', 'type', 'logo', 'description']


class HRContactInfoForm(ModelForm):
    personal_title = forms.IntegerField(
        widget=RadioSelect(
            attrs={'class': 'radioChoice'}, choices=HRContactInfo.PERSONAL_TITLE))
    preferred_contact = forms.IntegerField(
        widget=RadioSelect(
            attrs={'class': 'radioChoice'}, choices=HRContactInfo.PREF_CONTACT_TYPE))

    def clean_phoneNumber(self):
        phoneno = self.cleaned_data.get('phoneNumber')
        if self.cleaned_data.get('preferred_contact') == 2:
            if phoneno is None or phoneno == "":
                raise forms.ValidationError("Preferred contact cannot be Empty!")
            if not re.match(r'^\+?1?\d{10,15}$', phoneno):
                raise forms.ValidationError("Phone number should have 10-15 characters")
        return phoneno

    class Meta:
        model = HRContactInfo
        fields = '__all__'
        exclude = ['company']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Id'}),
            'preferred_contact': forms.RadioSelect(
                attrs={'class': 'form-radio', 'placeholder': 'Preferred Contact Type'})
        }


class RoleInfoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company_id', '')
        super(RoleInfoForm, self).__init__(*args, **kwargs)
        self.fields['criteria'] = forms.ModelChoiceField(queryset=Criteria.objects.filter(company_id=company_id))

    class Meta:
        model = CompanyJob
        fields = '__all__'
        exclude = ['company']


class JobCriteriaForm(ModelForm):
    batch = forms.ModelMultipleChoiceField(
        queryset=getInterviewAllowedBatches(),
        widget=forms.SelectMultiple()
    )

    class Meta:
        model = Criteria
        fields = '__all__'
        exclude = ['company']
