from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.forms.models import model_to_dict

from models import SurveyPub, SurveyPriv


def index(request):
    return redirect("http://www.iconz-webvisions.com/", permanent=True)


def fill(request, code):
    priv = get_object_or_404(SurveyPriv, code=code)
    pub = priv.pub

    if priv.complete:
        raise Http404

    return render(request, 'survey/' + pub.TEMPLATE, {'code': code})


def post(request, code):
    priv = get_object_or_404(SurveyPriv, code=code)
    pub = priv.pub
    pub_dict = pub.model_to_dict(pub)

    try:
        for key, value in pub_dict:
            pub(key=request.post[key])
    except KeyError:
        return render(request, 'survey/fill.html',
            {'code': code, 'error_message': 'Please ensure the form is complete.'})

    pub.save()

    priv.complete = True
    priv.save()

    return render(request, 'survey/thanks.html')