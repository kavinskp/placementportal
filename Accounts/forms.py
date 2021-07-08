from django.forms import ModelForm
from django import forms

from .models import *


class SignupForm(ModelForm):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.RadioSelect(choices=CustomUser.USER_TYPE_CHOICES)
    department = forms.ChoiceField(choices=Department.objects.all())

    class Meta:
        model = CustomUser
        fields = ('email', 'user_type')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            CustomUser.objects.get(email__iexact=email)
            raise forms.ValidationError('email already exists')
        except CustomUser.DoesNotExist:
            return email

    def clean_password2(self):
        pw1 = self.cleaned_data.get('password1')
        pw2 = self.cleaned_data.get('password2')
        if pw1 and pw2 and pw1 == pw2:
            return pw2
        raise forms.ValidationError("passwords don't match")

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            user_type = self.cleaned_data['user_type']
            department = self.cleaned_data['department']
            if user_type == 1:
                hod = HOD.objects.create(user=user, has_filled_profile=False, department=department)
                hod.save()
            if user_type == 2:
                staff = Staff.objects.create(user=user, has_filled_profile=False, department=department)
                staff.save()
            if user_type == 1:
                student = Student.objects.create(user=user, has_filled_profile=False, department=department)
                student.save()
        return user
