from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse

class ScrumUser(AbstractUser):
	@property
	def score(self):
	    return UserContent.objects.filter(author=self).aggregate(Sum('denorm_score'))['denorm_score__sum'] or 0

	denorm_score = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		self.denorm_score = self.score
		super(ScrumUser, self).save(*args, **kwargs)
	
	# Easy mode
	def set_password(self, raw_password):
		self.password = raw_password
		self._password = raw_password

	def check_password(self, raw_password):
		return self.password == raw_password

class UserContent(models.Model):
	author = models.ForeignKey(ScrumUser)
	text = models.TextField(blank=False)
	denorm_score = models.IntegerField(default=0)

	def set_vote(self, user, direction):
		Vote.objects.filter(voter=user, content=self).delete()
		Vote.objects.create(voter=user, content=self, direction=direction)
		self.save()

	@property
	def score(self):
	    return Vote.objects.filter(content=self).aggregate(Sum('direction'))['direction__sum'] or 0
	
	def save(self, *args, **kwargs):
		self.denorm_score = self.score
		super(UserContent, self).save(*args, **kwargs)

class Vote(models.Model):
	content = models.ForeignKey(UserContent)
	voter = models.ForeignKey(ScrumUser)
	direction = models.IntegerField()

	def save(self, *args, **kwargs):
		super(Vote, self).save(*args, **kwargs)
		self.content.save()
		self.voter.save()

	class Meta:
		unique_together = ['content', 'voter']

class Post(UserContent):
	title = models.TextField(blank=False)
	url = models.URLField(blank=True)

	def get_view_url(self):
		return reverse('view_post', args=[self.id])

class Comment(UserContent):
	parent = models.ForeignKey(Post, related_name='comments')
