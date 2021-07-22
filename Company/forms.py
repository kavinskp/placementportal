from django.forms import ModelForm
from django import forms
from .models import Company, HRContactInfo
from django.forms.widgets import TextInput, RadioSelect
import re


class CreateCompanyInfo(ModelForm):
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
        model = Company
        fields = ['name', 'fullName', 'website', 'type', 'logo', 'description']


class CreateHRContactInfo(ModelForm):
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
            if phoneno is None or phoneno is "":
                raise forms.ValidationError("Preferred contact cannot be Empty!")
            if not re.match(r'^\+?1?\d{10,15}$', phoneno):
                raise forms.ValidationError("Phone number should have 10-15 characters")
        return phoneno

    class Meta:
        model = HRContactInfo
        fields = '__all__'
        exclude = ('company', '')
