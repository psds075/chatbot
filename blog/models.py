from django.db import models
from django.utils import timezone

class Post(models.Model):
	author = models.ForeignKey('auth.User',on_delete=models.CASCADE) #on_delete는 삭제시 취할 수 있는 행동을 의미한다.
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title