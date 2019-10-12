from django.contrib import admin
from .models import User,Grievant,Department,Complaint
# Register your models here.
admin.site.register(User)
admin.site.register(Grievant)
admin.site.register(Complaint)
admin.site.register(Department)
