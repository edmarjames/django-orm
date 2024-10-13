from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from .models import Student


@receiver(pre_delete, sender=Student)
def pre_delete_profile(sender, **kwargs):
    print("You are about to delete a student profile")

@receiver(post_delete, sender=Student)
def post_delete_profile(sender, **kwargs):
    print("You have just deleted a student profile")