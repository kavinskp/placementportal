from django.forms import ModelForm
from django.core.mail import send_mail
from django import forms
import re
from PlacementPortal import settings
from .models import *


class LoginForm(forms.Form):
    email = forms.CharField(max_length=256)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has not been registered yet")
        return email

    def clean_password(self):
        return self.cleaned_data.get('password')


class SignupForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if CustomUser.objects.filter(email=email):
            raise forms.ValidationError("This email id has already been registered")
        return email

    def clean_password1(self):
        pw1 = self.cleaned_data.get('password1')
        if not re.match(r'(?=.*\d)(?=.*[a-zA-Z]).{6,}', pw1):
            raise forms.ValidationError(
                "Password should contains atleast 6 characters as well as a digit & a character")
        return pw1

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password2')
        if not re.match(r'(?=.*\d)(?=.*[a-zA-Z]).{6,}', pw1):
            raise forms.ValidationError(
                "Password should contains atleast 6 characters as well as a digit & a character")
        return pw1

    def clean_password(self):
        pw1 = self.clean_password1()
        pw2 = self.clean_password2()
        if pw1 and pw2 and pw1 == pw2:
            return pw2
        raise forms.ValidationError("Passwords don't match")

    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')
        exclude = (
            'is_approved',
            'is_verified'
        )

    def sendEmail(self, datas):
        link = settings.CURRENT_HOST_NAME + 'activate/' + datas['activation_key']
        subject = 'Placement Portal - Account Verification'
        message = 'Welcome to Placement Portal /n Click the following link to verify your account ' + link
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [datas['email']], fail_silently=False)


class DateInput(forms.DateInput):
    input_type = 'date'


class UpdateProfileStaff(ModelForm):

    def clean_designation(self):
        designation = self.cleaned_data.get('designation')
        if designation > 1:
            return designation
        raise forms.ValidationError('Choose proper designation')

    class Meta:
        model = Staff
        widgets = {
            'dob': DateInput(),
        }
        fields = '__all__'
        exclude = ['user']


class UpdateProfileStudent(ModelForm):

    class Meta:
        model = Student
        widgets = {
            'dob': DateInput(),
        }
        fields = '__all__'
        exclude = ['user']
