from re import U
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from notifications.models import Notification
from account.models import Profile

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
    likes_count = models.PositiveIntegerField(default=0)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='classes_liked', blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super(Class, self).save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title) + "-" + str(self.id)
            self.save()



class Likes(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
	dance_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_like')

	def user_liked_post(sender, instance, *args, **kwargs):
		like = instance
		dance_class = like.dance_class
		sender = like.user
                
		notify = Notification(dance_class=dance_class, sender=sender, user=dance_class.teacher, notification_type=1, sender_profile=Profile.objects.get(user=sender))
		notify.save()

	def user_unlike_post(sender, instance, *args, **kwargs):
		like = instance
		dance_class = like.dance_class
		sender = like.user

		notify = Notification.objects.filter(dance_class=dance_class, sender=sender, notification_type=1, sender_profile=Profile.objects.get(user=sender))
		notify.delete()
                

#Likes
post_save.connect(Likes.user_liked_post, sender=Likes)
post_delete.connect(Likes.user_unlike_post, sender=Likes)