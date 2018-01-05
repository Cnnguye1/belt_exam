from __future__ import unicode_literals
from datetime import datetime, date
from django.db import models
from django.utils.dateformat import DateFormat, TimeFormat
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')



# Create your models here.
class UserManager(models.Manager):
	def validateUser(self, post_data):
		now = datetime.now().strftime("%Y-%m-%d")
		errors = {}
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = '{} field is required'.format(field)
			if field == 'name' or field == 'alias':
				if not field in errors and len(value) < 3:
					errors[field] = '{} field must be at least 3 characters'.format(field)
			if field == 'password':
				if not field in errors and len(value)<8:
					errors[field] = '{} field must be at least 8 characters'.format(field)
			if field == 'confirm_pw':
				if not field in errors and post_data['password'] != post_data['confirm_pw']:
					if len(value) <1:
						pass
					else:
						errors['comfirm_pw'] = 'invalid comfirm password'

		if not 'email' in errors and not EMAIL_REGEX.match(post_data['email']):
			errors['email'] = 'invalid email'
		# if post_data['password'] != post_data['confirm_pw']:
		# 	if len(post_data['comfirm_pw']) < 1:
		# 		pass
		# 	else:
		# 		errors['comfirm_pw'] = 'invalid comfirm password'

		# print datetime.strftime(post_data['dob'], "%Y-%m-%d")
		if  not 'dob' in errors:
			today = date.today()
			born = datetime.strptime(str(post_data['dob']), "%Y-%m-%d" ).date()
			try:
				birthday = born.replace(year=today.year)
			except ValueError: # raised when birth date is February 29 and the current year is not a leap year
				birthday = born.replace(year=today.year, day=born.day-1)
			if birthday > today:
				age = today.year - born.year - 1
			else:
				age = today.year - born.year
			if not 'dob' in errors and age < 18:
				errors['dob'] = 'invalid Date of Birth. Must be 18 or Over'
		return errors
	def validateLogin(self, post_data):
		errors = {}
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = '{} field is required'.format(field)
			if field == 'email':
				if not 'email' in errors and not EMAIL_REGEX.match(post_data['email']):
					errors['email'] = 'invalid email'
			if field == 'password':
				if not field in errors and len(value)<8:
					errors[field] = '{} field must be at least 8 characters'.format(field)
		return errors

class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField(null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
	def __str__(self):
		return self.name