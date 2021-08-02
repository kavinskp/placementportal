from django.forms import ModelForm
from django import forms
from django.forms.widgets import RadioSelect

from dal import autocomplete

from Company.models import CompanyInfo, HRContactInfo, CompanyInterview, Criteria, JobRoles
from Accounts.views.utils import getInterviewAllowedBatches
import re


class CompanyInfoForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Short Name'}))
    fullName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Full Name'}))
    logo = forms.ImageField(required=False)
    website = forms.URLField(max_length=200,
                             initial="https://",
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Home Page URL'}))

    class Meta:
        model = CompanyInfo
        fields = ['name', 'fullName', 'website', 'type', 'logo', 'description']


class HRContactInfoForm(ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    middle_name = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    designation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Designation'}))
    phoneNumber = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Name'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    preferred_contact = forms.IntegerField(
        widget=RadioSelect(attrs={'class': 'radioChoice'}, choices=HRContactInfo.PREF_CONTACT_TYPE))

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


class RoleInfoForm(ModelForm):

    class Meta:
        model = JobRoles
        fields = '__all__'
        exclude = ['company']


class JobCriteriaForm(ModelForm):
    batch = forms.ModelMultipleChoiceField(
        queryset=getInterviewAllowedBatches(),
        widget=autocomplete.ModelSelect2Multiple()
    )

    class Meta:
        model = Criteria
        fields = '__all__'
        exclude = ['company']
