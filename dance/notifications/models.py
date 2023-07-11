from django.db import models
from django.contrib.auth.models import User
from account.models import Profile

class Notification(models.Model):
	NOTIFICATION_TYPES = ((1,'Like'),(2,'Comment'), (3,'Follow'))

	dance_class = models.ForeignKey('class.Class', on_delete=models.CASCADE, related_name="noti_class", blank=True, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="noti_from_profile",default=None)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
	text_preview = models.CharField(max_length=90, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)

	def __str__(self):
		return str(self.dance_class) + " was " + self.NOTIFICATION_TYPES[self.notification_type-1][1] + "ed by " + self.sender.username
	
	
