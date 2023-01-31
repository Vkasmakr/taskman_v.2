from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee

#
# # Sukūrus vartotoją auto sukuriamas profilis
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)


# Išsaugoti korekcijas vartotojo
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.employee.save()
