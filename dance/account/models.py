from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

ROLE_CHOICES = (('TEACHER', 'Teacher'), ('STUDENT', 'Student'))

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete = models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    description = models.TextField()
    type = models.CharField(choices = ROLE_CHOICES, max_length=10)

    def __str__(self):
        return f'Profile of {self.user.username}'