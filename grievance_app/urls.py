from . import views
from django.urls import path

urlpatterns = [
path('',views.Index.as_view(),name='index'),
path('student_register/',views.grievant_register,name='student_register'),
path('department_register/',views.department_register,name='department_register'),
path('user_login/',views.user_login,name='user_login'),
path('user_logout/',views.user_logout,name='user_logout'),
path('grievant_complaint_list/<int:pk>/',views.GrievantComplaintListView.as_view(),name='grievant_complaint_list'),
path('department_complaint_list/<int:pk>/',views.DepartmentComplaintListView.as_view(),name='department_complaint_list'),
path('complaint/new/',views.CreateComplaintView.as_view(),name='create_complaint'),
path('complaint_detail/<int:pk>/',views.ComplaintDetailView.as_view(),name='complaint_detail'),
path('update_complaint/<int:pk>/',views.UpdateComplaintView.as_view(),name='update_complaint'),
]
