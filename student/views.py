from .models import (
    Product,
    Student,
    Teacher,
)
from django.db import (
    connection,
    transaction
)
from django.db.models import (
    Avg,
    Max,
    Min,
    Q,
    Sum,
)
from django.shortcuts import render
from .forms import ClassroomUpdateForm


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


# Part 5
#################################################################
def student_list_not(request):
    # You can use exclude and "&" symbol to create complex not query
    # not_post = Student.objects.exclude(surname__startswith="Bautista") & Student.objects.exclude(age__gt=23)

    # You can also simplify it using tilde symbol "~" as NOT together with the "Q" object
    not_post = Student.objects.filter(~Q(surname__startswith="Bautista") & ~Q(age__gt=23))

    print(not_post)
    print(connection.queries)

    context = {
        "not_post": not_post
    }

    return render(request, "output.html", context)


# Part 6 Select & Output Individual Fields
#################################################################
def student_list_select(request):
    # Use "only" to get specific fields from the table
    select_post = Student.objects.filter(classroom=1).only("firstname", "age")

    print(select_post)
    print(connection.queries)

    context = {
        "select_post": select_post
    }

    return render(request, "output.html", context)


# Part 7 Raw SQL queries
#################################################################
def student_list_raw(request):
    # Using Django ORM
    # all_post = Student.objects.all()

    # Using "raw" to perform raw sql queries
    raw_post = Student.objects.raw("SELECT * FROM student_student WHERE age=26")

    print(raw_post)
    print(connection.queries)

    context = {
        "raw_post": raw_post
    }

    return render(request, "output.html", context)


# Part 8 Simple Bypassing ORM
#################################################################
def dict_fetchall(cursor):
    """Helper function for converting the result of query to a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

def student_list_raw_sql(request):
    # This will allow you to use the cursor object
    cursor = connection.cursor()

    # This is where you define your SQL query
    cursor.execute("SELECT * FROM student_student WHERE age > 23")

    # Output the data using helper function
    r = dict_fetchall(cursor)

    # Alternative method
    # r = cursor.fetchall()

    print(r)
    print(connection.queries)

    context = {
        "raw_sql_count": r
    }

    return render(request, "output.html", context)


# Part 13 Transaction Atomicity
#################################################################
def student_list_atomic(request):
    all_student = Student.objects.all()
    students = []
    error = ""

    print(all_student)
    print(connection.queries)

    if request.method == "POST":
        form = ClassroomUpdateForm(request.POST)

        if form.is_valid() == True:
            student_one = form.cleaned_data["studentone"]
            student_two = form.cleaned_data["studenttwo"]
            classroom = form.cleaned_data["classroom"]

            students = [student_one, student_two]
        else:
            form = ClassroomUpdateForm()

    if students:
        try:
            # Used transaction.atomic to guarantee that either all of the transaction succeeds or none of it does.
            with transaction.atomic():
                for student in students:
                    student_record = Student.objects.get(firstname=student.title())
                    student_record.classroom = classroom
                    student_record.save()
        except:
            error = "An exception occurred"

    context = {
        "all_student": all_student,
        "error": error
    }

    return render(request, "output.html", context)


# Part 15 Aggregation
#################################################################
def student_list_aggregate(request):

    product_data = Product.objects.aggregate(total=Sum("price"), mini=Min("price"),
                                             maxi=Max("price"), aveg=Avg("price"))

    print(product_data)
    print(connection.queries)

    context = {
        "product_data": product_data,
    }

    return render(request, "output.html", context)