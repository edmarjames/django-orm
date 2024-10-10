from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [
    path('', views.student_list, name='student_data'),
    path('and/', views.student_list_and, name='student_data_and'),
    path('union/', views.student_list_union, name='student_data_union'),
    path('not/', views.student_list_not, name='student_data_not'),
    path('select/', views.student_list_select, name='student_data_select'),
    path('raw/', views.student_list_raw, name='student_data_raw'),
    path('raw_sql/', views.student_list_raw_sql, name='student_data_raw_sql'),
    path('atomic/', views.student_list_atomic, name='student_data_atomic'),
    path('aggregate/', views.student_list_aggregate, name='student_data_aggregate')
]
