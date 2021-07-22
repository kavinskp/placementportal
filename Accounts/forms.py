from django.forms import ModelForm
from django.forms.widgets import RadioSelect
from django.core.mail import send_mail
from django import forms
import re

from PlacementPortal import settings
from Accounts.models import UserProfile, StaffAccount, CustomUser, GENDER_CHOICES
from Curriculum.models import StudentInfo
from Company.models import Company


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


USER_TYPE_CHOICES = (
    (2, 'Staff'),
    (3, 'Student'),
    (4, 'Interviewer'),
)


class SignupForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password (Again)'}))
    user_type = forms.IntegerField(
        widget=RadioSelect(attrs={'class': 'radioChoice'}, choices=USER_TYPE_CHOICES))

    def clean_email(self):
        cd = self.cleaned_data
        email = cd.get('email')
        if not re.match(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', email):
            raise forms.ValidationError("Please enter a valid email id")
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
        fields = ('email', 'password1', 'password2', 'user_type')

    def sendEmail(self, datas):
        link = settings.CURRENT_HOST_NAME + 'activate/' + datas['activation_key']
        subject = 'Placement Portal - Account Verification'
        message = 'Welcome to Placement Portal /n Click the following link to verify your account ' + link
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [datas['email']], fail_silently=False)


class DateInput(forms.DateInput):
    input_type = 'date'


class UserProfileForm(ModelForm):
    gender = forms.CharField(
        widget=RadioSelect(attrs={'class': 'radioChoice'}, choices=GENDER_CHOICES))

    class Meta:
        model = UserProfile
        fields = '__all__'
        widgets = {
            'dob': DateInput(),
        }


class StaffAccountForm(ModelForm):
    class Meta:
        model = StaffAccount
        fields = '__all__'
        exclude = ['user', 'designation']


class StudentInfoForm(ModelForm):
    class Meta:
        model = StudentInfo
        fields = '__all__'
