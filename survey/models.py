from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from emailer import send_email

import string
import random

#Public stuff
class SurveyPub(models.Model):
	priv = models.OneToOneField('SurveyPriv', related_name='pub')

	class Meta:
		abstract = True	

class CustCareSurveyA(SurveyPub):
	TEMPLATE = "custCareFormA.html"

	RATING_CHOICES = (('None', None), (0, 0), (1, 1), (2, 2), (3, 3))
	rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
	comment = models.TextField(blank=True)
	first_time_res = models.NullBooleanField(blank=True, null=True)

#Internal stuff
class SurveyPriv(models.Model):
	EMAIL_TEMPLATES = (('custCareEmailA', 'custCareA'), ('fake', 'fake'))

	email_template = models.CharField(max_length=64, choices=EMAIL_TEMPLATES, blank=True)
	email_address = models.CharField(max_length=254)
	email_sent = models.BooleanField(default=False)

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
	complete = models.BooleanField()

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
		if not self.email_sent:
			send_email(self)
			self.email_sent = True

		super(SurveyPriv, self).save(*args, **kwargs)