from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class UserContent(models.Model):
	author = models.ForeignKey(User)
	text = models.TextField(blank=False)

	def set_vote(self, user, direction):
		Vote.objects.filter(voter=user, content=self).delete()
		Vote.objects.create(voter=user, content=self, direction=direction)

	@property
	def score(self):
	    return Vote.objects.filter(content=self).aggregate(Sum('direction'))['direction__sum'] or 0
	

class Vote(models.Model):
	content = models.ForeignKey(UserContent)
	voter = models.ForeignKey(User)
	direction = models.IntegerField()
	class Meta:
		unique_together = ['content', 'voter']

class Post(UserContent):
	title = models.TextField(blank=False)
	url = models.URLField(blank=True)

	def get_view_url(self):
		return reverse('view_post', args=[self.id])

class Comment(UserContent):
	parent = models.ForeignKey(Post, related_name='posts')
