from .models import (
    Student,
    Teacher
)
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

    return render(request, "output.html", {"posts":posts})

def student_list(request):
    # This query use the "|" symbol as "OR"
    # posts = Student.objects.filter(surname__startswith='Bautista') | Student.objects.filter(surname__startswith='Doe')

    # It can be simplified using "Q" objects together with the "|" symbol as OR
    posts = Student.objects.filter(Q(surname__startswith="Bautista") | Q(surname__startswith="Doe"))

    # Use can use tilde symbol "~" as not together with the "Q" object
    not_posts = Student.objects.filter(Q(surname__startswith="Bautista") | ~Q(surname__startswith="Doe"))

    print(posts)
    print(connection.queries)

    context = {
        "posts": posts,
        "not_posts": not_posts
    }

    return render(request, "output.html", context)


# Part 3
#################################################################
def student_list_and(request):
    # This query use the "&" symbol as "AND"
    # and_post = Student.objects.filter(classroom=3) & Student.objects.filter(firstname__startswith='Jane')

    # It can be simplified using "Q" objects together with the "&" symbol as AND
    and_post = Student.objects.filter(Q(classroom=3) & Q(firstname__startswith="Jane"))

    print(and_post)
    print(connection.queries)

    context = {
        "and_post": and_post
    }

    return render(request, "output.html", context)


# Part 4
#################################################################
def student_list_union(request):
    # Union is used to combine the results of two select query
    # Union remove duplicates from the two combined query
    union_post = Student.objects.all().values_list("firstname").union(Teacher.objects.all().values_list("firstname"))

    print(union_post)
    print(connection.queries)

    context = {
        "union_post": union_post
    }

    return render(request, "output.html", context)