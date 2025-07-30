from django.db import models
from django.utils.translation import gettext_lazy as _

class DeleteModel(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)



class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    is_deleted = models.BooleanField(default=False)

    objects=DeleteModel()
    new=models.Manager()

    class Meta:
        abstract = True

    def delete(self,*args, **kwargs):
        self.is_deleted = True
        self.save(*args,**kwargs)

class Author(BaseModel):
    full_name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    @property
    def cuntry_name(self):
        return f'{self.full_name} {self.country}'

    def __str__(self):
        return self.full_name


class Book(BaseModel):
    title = models.CharField(_('title'),max_length=300)
    slug = models.SlugField(_('slug'),max_length=300, unique=True)
    description = models.TextField(_('description'),blank=True,null=True)
    price = models.IntegerField(_('price'),blank=True, null=True)
    quantity = models.IntegerField(_('quantity'),blank=True, null=True)
    total = models.PositiveIntegerField(_('total'),blank=True, null=True)
    published_year = models.DateField(_('published_year'),null=True, blank=True)
    image = models.ImageField(_('image'),null=True, blank=True, upload_to="images/")
    file = models.FileField(_('file'),null=True, blank=True, upload_to="images/")
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='book_author', blank=True, null=True)


    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)

    @property
    def total_p(self):
        if self.quantity is None:
            return 0
        else:
            return self.price * self.quantity



    def __str__(self):
        return self.title

