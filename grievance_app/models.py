from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    is_grievant = models.BooleanField(default=False)
    is_department = models.BooleanField(default=False)

class Grievant(models.Model):
    student = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    Registeration = models.IntegerField(default=0000)
    Room = models.CharField(max_length=50)
    Hostel = models.CharField(max_length=100)

    def __str__(self):
        return self.student.username

class Department(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    choices = [('Pl','Plumbing'),('Ca','Carpentry'),('El','Electricity'),('La','Lan Network')]
    department_name = models.CharField(choices=choices,max_length=2,default='Pl')

    def __str__(self):
        return self.get_department_name_display()


class Complaint(models.Model):
    grievant = models.ForeignKey('grievance_app.Grievant',on_delete=models.CASCADE,related_name='complaintee')
    department = models.ForeignKey('grievance_app.Department',on_delete=models.CASCADE)
    text = models.TextField()
    heading = models.CharField(max_length=200,blank=False,null=False,default='Problem')
    media = models.ImageField(upload_to='complaints_image',blank=True)
    created_date = models.DateTimeField(default=timezone.now())
    status_choices = [('D','Done'),('P','Pending'),('N','Not Accepted')]
    status = models.CharField(choices=status_choices,max_length=1,default='N')

    class Meta():
        verbose_name_plural = 'Complaints'

    def change_status(self,choice):
        self.status = choice
        self.save()

    def __str__(self):
        return self.heading

    def get_absolute_url(self):
        return reverse("complaint_detail",kwargs={'pk':self.pk})
