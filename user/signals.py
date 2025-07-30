from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from user.models import CustomUser, Profile


@receiver(post_save, sender=CustomUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        print(f"{instance.username} nomli user yaradi")


@receiver(pre_delete, sender=CustomUser)
def cutomuser_pre_delete(sender, instance, **kwargs):
    if instance:
        print(f"{instance.username} nomli cutomuser delete qilindi ")



@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()