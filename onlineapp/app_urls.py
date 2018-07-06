from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from onlineapp.views import *
from onlineapp.views.Auth import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    path('colleges/', CollegeView.as_view(), name='colleges_list'),
    path('colleges/<str:acronym>/', CollegeResults.as_view(), name="college_details"),
    path('addcollege', CreateCollegeView.as_view(), name="add_college"),

    path('colleges/<str:acronym>/addstudent/', CreateStudentView.as_view()),
    path('colleges/<int:pk>/edit/', EditCollegeView.as_view(), name="edit_college"),
    path('colleges/<int:pk>/delete/', DeleteCollegeView.as_view(), name="delete_college"),
    path('colleges/<str:acronym>/<int:pk>/delete/', DeleteStudentView.as_view(), name="delete_student"),
    path('colleges/<str:acronym>/<int:pk>/edit/', EditStudentView.as_view(), name="edit_student"),

    path('api/v1/colleges/', CollegeApiAllView.as_view(), name='colleges_all_api'),
    path('api/v1/colleges/<int:pk>/', CollegeApiView.as_view(), name='college_single_api'),
    path('api/v1/colleges/students/', StudentDetailsApiView.as_view(), name='students_all_api'),
    path('api/v1/colleges/<int:pk>/students/', StudentDetailsApiView.as_view(), name='students_from_college_api'),
    path('api/v1/colleges/<int:pk>/students/<int:spk>/', StudentDetailsApiView.as_view(), name='student_api'),
    url(r'^api-token-auth/', obtain_jwt_token),
]
