from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_list, name='student_data'),
    path('and/', views.student_list_and, name='student_data_and'),
    path('union/', views.student_list_union, name='student_data_union')
]
