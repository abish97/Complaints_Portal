from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Complaint,Department,Grievant,User

class ComplaintForm(forms.ModelForm):

    class Meta():
        model = Complaint
        fields = ('department','heading','text','media',)

class UpdateComplaintForm(forms.ModelForm):

    class Meta():
        model = Complaint
        fields = ('status',)

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password')


class GrievantProfileForm(forms.ModelForm):

    class Meta():
        model = Grievant
        fields = ('Registeration','Room','Hostel')


class DepartmentProfileForm(forms.ModelForm):

    class Meta():
        model = Department
        fields = ('department_name',)
