from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField

# Create your models here.
class Class(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now=True)
    planned_date = models.DateTimeField()
    description = models.TextField()
    teacher = models.ForeignKey(User, related_name='classes_created', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='classes_joined', blank=True)
    address = models.CharField(max_length=500, default=None)
    video_url = EmbedVideoField(blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Class, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()
