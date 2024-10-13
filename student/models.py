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


# Foreign key deletion contstraint
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Warranty(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="product_category")
    manufacturer = models.ForeignKey(Manufacturer, null=True, blank=True, on_delete=models.CASCADE, related_name="product_manufacturer")
    warranty = models.ForeignKey(Warranty, null=True, blank=True, on_delete=models.PROTECT, related_name="product_warranty")

    def __str__(self):
        return f"{self.name} - {self.category}"

# Using SET_NULL will set the value of the "category "field to null if the value of the foreignKey is deleted on the parent table.

# Using SET_DEFAULT will set the value of the field to the set default value when the foreignKey is deleted.

# Using CASCADE will also delete the value of "manufacturer" when the foreignKey is deleted.

# using PROTECT will not allow the deletion of foreignKey unless the related objects are already deleted.

# using RESTRICT is the same with PROTECT.

# using SET will set the value of the field based on the returned value of the function you specify to use.

# using DO_NOTHING will do nothing if the foreignKey is deleted.