from django.contrib.auth.models import User
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify

from book.models import Book


@receiver(pre_save, sender=Book)
def book_pre_save( sender,instance, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.title)
        print(instance.slug)


@receiver(pre_delete, sender=Book)
def book_pre_delete(sender, instance, **kwargs):
    if instance:
        print(f"{instance.title} nomli book delete qilindi ")