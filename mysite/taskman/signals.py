from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# For saving Employee configuration
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.employee.save()
