# from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.urls import reverse
from django.views import generic

# Create your views here.
# def index(request):
#     lt_list = Question.objects.order_by('-pub_date')[:5]
#
#     context = {
#     'lt_list' : lt_list
#     }
#     return render(request,'polls/index.html',context)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lt_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
# def detail(request,question_id):
#     # try:
#     #     question=Question.objects.get(pk =question_id)
#     # except Exception as e:
#     #     raise Http404('Nope not there!!')
#     question = get_object_or_404(Question,pk =question_id )
#     return render(request,'polls/details.html',{'question' : question})
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

# def results(request,question_id):
#     question = get_object_or_404(Question,pk =question_id )
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#     return render(request, 'polls/results.html', {'question': question})



def vote(request,question_id):
    question = get_object_or_404(Question,pk =question_id )
    try:
        # get selectrf choice
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError,Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes +=1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
