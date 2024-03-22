from django.db import models
from Main_App.models import BaseModel
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _



# Create your models here.
class NavigationItem(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    link = models.CharField(max_length=200,verbose_name=_('Link'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name=_('Parent'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    

    class Meta:
        ordering = ['position',]

    def __str__(self):
        return self.title
    

class PageModel(BaseModel):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=250
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True
    )

    content = RichTextField(
        verbose_name=_('Content')
    )

    feature_image = models.ImageField(
        upload_to='page_images',
        verbose_name=_('Featured Image'),
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(PageModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('page', args=[str(self.slug)])