from django.db import models
from django.utils import timezone

# Model Tasks 1-5
#####################################

class Teacher(models.Model):

    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

class Student(models.Model):

    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    classroom = models.IntegerField()
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname

######################################

# Proxy models
# Change the behavior of a model
# Proxy models operate on the original model
class BookContent(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class BookOrders(BookContent):
    class Meta:
        proxy = True
        ordering = ["created"]

    def created_on(self):
        return timezone.now() - self.created


# Multi table model inheritance
# Every model is a model all by itself
# One to one link is created automatically
class Books(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class ISBN(Books):
    books_ptr = models.OneToOneField(
        Books, on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
    )
    ISBN = models.TextField()


# Abstract Model
# Used when you have common information needed for number of other models
class BaseItem(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["title"]

class ItemA(BaseItem):
    content = models.TextField()

    class Meta(BaseItem.Meta):
        ordering = ["-created"]

class ItemB(BaseItem):
    file = models.FileField(upload_to="files")

class ItemC(BaseItem):
    file = models.FileField(upload_to="images")

class ItemD(BaseItem):
    slug = models.SlugField(max_length=255, unique=True)