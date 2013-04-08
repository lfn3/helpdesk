from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def send_email(SurveyPriv):
	context = Context({'code': SurveyPriv.code})

	plain_text = get_template(SurveyPriv.email_template + '.txt').render(context)
	html = get_template(SurveyPriv.email_template + '.html').render(context)

	message = EmailMultiAlternatives('iWV Helpdesk Survey', plain_text, 'ICONZ-Webvisions Customer Care <support.nz@iconz-webvisions.com>', [SurveyPriv.email_address])
	message.attach_alternative(html, "text/html")
	message.send()