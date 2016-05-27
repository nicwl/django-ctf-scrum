from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class UserContent(models.Model):
	author = models.ForeignKey(User)
	text = models.TextField(blank=False)

	def set_vote(self, user, direction):
		Vote.objects.filter(user=user, content=self).delete()
		Vote.objects.create(user=user, content=self, direction=direction)

	@property
	def score(self):
	    return Vote.objects.filter(content=self).aggregate(Sum('direction'))['direction__sum']
	

class Vote(models.Model):
	content = models.ForeignKey(UserContent)
	voter = models.ForeignKey(User)
	direction = models.IntegerField()
	class Meta:
		unique_together = ['content', 'voter']

class Post(UserContent):
	title = models.TextField(blank=False)
	url = models.URLField(blank=True)

class Comment(UserContent):
	parent = models.ForeignKey(Post, related_name='posts')
