from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.forms.models import model_to_dict
from django.utils.timezone import utc

from models import SurveyPub, SurveyPriv

def index(request):
    return redirect("http://www.iconz-webvisions.com/", permanent=True)


def fill(request, code):
    priv = get_object_or_404(SurveyPriv, code=code)
    pub = priv.pub

    if priv.is_completed():
        raise Http404

    return render(request, 'survey/' + pub.TEMPLATE, {'code': code})


def post(request, code):
    priv = get_object_or_404(SurveyPriv, code=code)
    pub = priv.pub
    pub_dict = model_to_dict(pub, exclude=['id', 'priv'])

    for key in pub_dict:
        pub_dict[key] = request.POST[key]
    
    pub = pub.__class__(id=pub.id, priv=pub.priv, **pub_dict)
    pub.save()

    priv.completed_on = timezone.now()
    priv.save()

    return render(request, 'survey/thanks.html')