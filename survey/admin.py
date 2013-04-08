from django.contrib import admin
from survey.models import SurveyPub, SurveyPriv

for subclass in SurveyPub.__subclasses__():
	admin.site.register(subclass)
admin.site.register(SurveyPriv)