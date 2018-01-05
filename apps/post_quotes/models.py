from __future__ import unicode_literals

from django.db import models
from ..login_reg.models import User
# Create your models here.
class QuoteManager(models.Manager):
	def validateQuote(self, post_data):
		errors = {}
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = '{} field is required'.format(field)
			if field == 'name':
				if not field in errors and len(value) < 3:
					errors[field] = '{} field must be at least 3 characters'.format(field)
			if field == 'message':
				if not field in errors and len(value) < 8:
					errors[field] = '{} field must be at least 8 characters'.format(field)
		return errors
		
class Quote(models.Model):
	name = models.CharField(max_length=255)
	message = models.TextField()
	post_by = models.ForeignKey(User, related_name='post_by')
	user_favorites = models.ManyToManyField(User, related_name='user_favorites')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = QuoteManager()
	def __str__(self):
		return self.name
		