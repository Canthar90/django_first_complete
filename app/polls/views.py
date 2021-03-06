from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Question, Choice


class IndexView(generic.ListView):
    """Creating polls index view"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions, not including thoseset to
        be published in future."""
        filtered = Question.objects.filter(choice__isnull=False,
        pub_date__lte=timezone.now()).distinct().order_by('-pub_date')[:5]
        return filtered

class DetailView(generic.DetailView):
    """making detail view page"""
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(choice__isnull=False,
            pub_date__lte=timezone.now()).distinct()

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet"""
        return Question.objects.filter(choice__isnull=False,
            pub_date__lte=timezone.now()).distinct()

def vote(request, question_id):
    """Creating vote page"""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
