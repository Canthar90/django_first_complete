from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader


from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, question_id):
    """ Shows question id """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404
    return render(request, "polls/detail.html", {'question':question})

def results(request, question_id):
    """Creating response page"""
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(requestm, question_id):
    """Creating vote page"""
    return HttpResponse("You're voting on question %s." % question_id)
