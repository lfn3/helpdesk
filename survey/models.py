from django.db import models
from emailer import send_email

import string
import random

#Public stuff
class SurveyPub(models.Model):
	RATING_CHOICES = ((0, 0), (1, 1),(2, 2),(3, 3),(4, 4))
	rating = models.IntegerField(choices=RATING_CHOICES)
	comment = models.TextField(blank=True)
	first_time_res = models.BooleanField()

	def __unicode__(self):
		return (str)(self.rating) + ': ' + self.comment[:64]

#Customer Care stuff
class SurveyPriv(models.Model):
	pub = models.ForeignKey(SurveyPub, null=True, blank=True)

	email_address = models.CharField(max_length=254)
	email_sent = models.BooleanField(default=False)

	def code_gen(length=4, chars=string.ascii_lowercase):
		return ''.join(random.choice(chars) for x in range(length))

	code = models.CharField(max_length=24, unique=True, default=code_gen)
	notes = models.TextField(blank=True)
	complete = models.BooleanField()

	def __unicode__(self):
		return self.code + ': ' + self.notes[:64]

	def save(self, *args, **kwargs):
		#Pretty hacky way of ensuring code is unique before we do the DB insert.
		#Will only fire on first save due to the if not self.pk line.
		if not self.pk:
			codeTest = False
			sanityCheck = 0
			while not codeTest:
				try:
					SurveyPriv.objects.get(code=self.code)
					self.code = code_gen(length = sanityCheck / 4 + 4)
					sanityCheck += 1

					while self.code is 'admin':
						self.code = code_gen(length = sanityCheck / 4 + 4)
				except SurveyPriv.DoesNotExist:
					codeTest = True

		#If email hasn't been sent... send it.
		if not self.email_sent:
			send_email(self)
			self.email_sent = True

		super(SurveyPriv, self).save(*args, **kwargs)


