from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'new_contact'
