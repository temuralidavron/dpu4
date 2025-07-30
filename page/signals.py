from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from page.models import Contact


@receiver(pre_save, sender=Contact)
def slug_create(sender, instance,  **kwargs):
    if instance:
        instance.slug=slugify(instance.name)
