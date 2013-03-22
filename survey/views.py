from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from models import SurveyPub, SurveyPriv

def index(request):
	return redirect("http://www.iconz-webvisions.com/", permanent=True)

def fill(request, code):
	priv = get_object_or_404(SurveyPriv, code=code)

	if priv.complete:
		raise Http404

	return render(request, 'survey/fill.html', {'code': code})

def post(request, code):
	priv = get_object_or_404(SurveyPriv, code=code)

	try:
		print(request.POST['comment'])
		pub = SurveyPub(first_time_res=request.POST['first_time_res'], rating=request.POST['rating'], comment=request.POST['comment'])
	except KeyError:
		return render(request, 'survey/fill.html', 
			{'code': code, 'error_message': 'Please ensure the form is complete.'})
	
	pub.save()

	priv.pub = pub
	priv.complete = True
	priv.save()

	return render(request, 'survey/thanks.html')