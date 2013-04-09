#!/usr/bin/python
# -*- coding: latin-1 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from emailer import send_email

import string
import random
from datetime import datetime

#Public stuff
class SurveyPub(models.Model):
	priv = models.OneToOneField('SurveyPriv', related_name='pub')

	class Meta:
		abstract = True	

	def __unicode__(self):
		return self.priv.email_address

class CustCareSurveyA(SurveyPub):
	TEMPLATE = "custCareFormA.html"

	RATING_CHOICES = (('None', None), (0, 0), (1, 1), (2, 2), (3, 3))
	rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
	customer_comment = models.TextField(blank=True)
	first_time_res = models.NullBooleanField(blank=True, null=True)

#Internal stuff
class SurveyPriv(models.Model):
	EMAIL_TEMPLATES = (('custCareEmailA', 'custCareA'),)

	email_template = models.CharField(max_length=64, choices=EMAIL_TEMPLATES, blank=True)
	email_address = models.CharField(max_length=254)
	email_sent_on = models.DateTimeField(blank=True, null=True, editable=False)

	def code_gen(length=4, chars=string.ascii_lowercase):
		code = ''.join(random.choice(chars) for x in range(length))
		codeTest = False
		sanityCheck = 0
		while not codeTest:
			try:
				SurveyPriv.objects.get(code=code) #This will throw an exception if not found
				code = code_gen(length = sanityCheck / 4 + 4)
				sanityCheck += 1

				while code is 'admin':
					code = code_gen(length = sanityCheck / 4 + 4)
			except SurveyPriv.DoesNotExist:
				codeTest = True	
		return code

	code = models.CharField(max_length=24, unique=True, default=code_gen)
	notes = models.TextField(blank=True)

	completed_on = models.DateTimeField(blank=True, null=True, editable=False)

	def save(self, *args, **kwargs):
		#Set email template if unset
		if self.email_template == "":
			self.email_template = random.choice(self.EMAIL_TEMPLATES)[0]

		super(SurveyPriv, self).save(*args, **kwargs)

		try:
			self.pub
		except:
			self.pub = random.choice(SurveyPub.__subclasses__())()
			self.pub.save()

		#If email hasn't been sent... send it.
		if not self.is_email_sent():
			try:
				send_email(self)
				self.email_sent_on = datetime.now()
			except SMTPAuthenticationError as e:
				pass

		super(SurveyPriv, self).save(*args, **kwargs)

	def is_completed(self):
		if self.completed_on != None:
			return True
		else:
			return False

	def is_email_sent(self):
		if self.email_sent_on != None:
			return True
		else:
			return False

	def __unicode__(self):
		return self.email_address