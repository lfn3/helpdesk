from django.contrib import admin, messages
from survey.models import SurveyPub, SurveyPriv

for subclass in SurveyPub.__subclasses__():
	admin.site.register(subclass)

class SurveyAdmin(admin.ModelAdmin):

	list_display = ('__unicode__', 'is_email_sent', 'is_completed', 'code')
	readonly_fields = ('is_email_sent', 'email_sent_on', 'is_completed', 'completed_on')

	def save_model(self, request, obj, form, change):
		super(SurveyAdmin, self).save_model(request, obj, form, change)

		if not obj.is_email_sent():
			messages.add_message(request, messages.WARNING, "Email failed to send. Retry by saving again.")

admin.site.register(SurveyPriv, SurveyAdmin)