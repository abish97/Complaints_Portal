from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.urls import reverse_lazy

from .forms import SignUpForm,GrievantProfileForm,DepartmentProfileForm,ComplaintForm,UpdateComplaintForm
from .models import User,Grievant,Department,Complaint
from .decorators import grievant_required,department_required
# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'

@method_decorator([login_required, grievant_required], name='dispatch')
class GrievantComplaintListView(ListView):
    login_url = '/login/'
    model = Complaint
    context_object_name = 'complaint_list'
    template_name = 'grievant_complaint_list.html'

    def get_queryset(self):
        student = Grievant.objects.get(student=self.request.user)
        complaint_list = Complaint.objects.filter(grievant=student)
        return complaint_list

@method_decorator([login_required,department_required], name='dispatch')
class DepartmentComplaintListView(ListView):
    login_url = '/login/'
    model = Complaint
    context_object_name = 'complaint_list'
    template_name = 'department_complaint_list.html'

    def get_queryset(self):
        department = Department.objects.get(user=self.request.user)
        complaint_list = Complaint.objects.filter(department=department)
        return complaint_list


@method_decorator([login_required,department_required],name='dispatch')
class UpdateComplaintView(UpdateView):
    login_url = '/login/'
    model = Complaint
    template_name = 'update_complaint.html'
    form_class = UpdateComplaintForm
    redirect_field_name = 'complaint_detail.html'


@method_decorator([login_required, grievant_required], name='dispatch')
class CreateComplaintView(CreateView):
    login_url = '/login/'
    redirect_field_name = 'complaint_detail.html'
    template_name = 'create_complaint.html'
    form_class = ComplaintForm

    model = Complaint

    def form_valid(self, ComplaintForm):
        student = Grievant.objects.get(student=self.request.user)
        ComplaintForm.instance.grievant = student
        return super().form_valid(ComplaintForm)


class ComplaintDetailView(LoginRequiredMixin,DetailView):
    login_url = '/login/'
    model = Complaint
    template_name = 'complaint_detail.html'


def grievant_register(request):

    registered = False

    if request.method == 'POST':
        if Grievant.objects.filter(Registeration=request.POST['Registeration']).count() >0:
            response = {}
            response['error'] = 'This Registeration Number already exists'
            return render(request,'student_register.html',response)
        user_form = SignUpForm(data=request.POST)
        profile_form = GrievantProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_grievant = True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
        return redirect('/')
    else:
        user_form = SignUpForm()
        profile_form = GrievantProfileForm()

    return render(request,'student_register.html',
                {'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered})

def department_register(request):

    registered = False

    if request.method == 'POST':
        if Department.objects.filter(department_name=request.POST['department_name']).count() >0:
            response = {}
            response['error'] = 'This Department already exists'
            return render(request,'department_register.html',response)
        user_form = SignUpForm(data=request.POST)
        profile_form = DepartmentProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.is_department = True
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
        return redirect('/')
    else:
        user_form = SignUpForm()
        profile_form = DepartmentProfileForm()

    return render(request,'department_register.html',
                {'user_form':user_form,
                'profile_form':profile_form,
                'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active and user.is_grievant:
                login(request,user)
                return HttpResponseRedirect(reverse('grievant_complaint_list',kwargs={'pk':user.id}))
            elif user.is_active and user.is_department:
                login(request,user)
                return HttpResponseRedirect(reverse('department_complaint_list',kwargs={'pk':user.id}))
            else:
                return HttpResponse('Account not active')
        else:
            return HttpResponse("Invalid Login Details")
    else:
        return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
