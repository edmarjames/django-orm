from .models import Student
from django.db import connection
from django.db.models import Q
from django.shortcuts import render

# Part 2
#################################################################
def student_list_(request):

    posts = Student.objects.all()

    print(">>> Raw queryset")
    print(posts)

    print(">>> Raw SQL query")
    print(posts.query)

    print(">>> Execution details")
    print(connection.queries)

    return render(request, 'output.html', {'posts':posts})

def student_list(request):
    # This query using the "|" symbol as "OR"
    # posts = Student.objects.filter(surname__startswith='Bautista') | Student.objects.filter(surname__startswith='Doe')

    # It can be simplified using "Q" objects together with the "|" symbol as OR
    posts = Student.objects.filter(Q(surname__startswith='Bautista') | Q(surname__startswith='Doe'))

    # Use can use tilde symbol "~" as not together with the "Q" object
    # posts = Student.objects.filter(Q(surname__startswith='Bautista') | ~Q(surname__startswith='Doe'))

    print(posts)
    print(connection.queries)

    return render(request, 'output.html', {'posts':posts})
