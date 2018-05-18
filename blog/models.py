from django.db import models
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #on_delete는 삭제시 취할 수 있는 행동을 의미한다.
	text = models.TextField(default='')
	created_date = models.DateTimeField(default=timezone.now)
	button = models.TextField(default='')

	def publish(self):
		self.created_date = timezone.now()
		self.save()

	def __str__(self):
		return self.text