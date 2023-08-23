from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
# from django.template import loader

from .models import Question, Choice

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     # template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list
#     }
#     # output = ", ".join([q.question_text for q in latest_question_list])
#     # return HttpResponse(template.render(context, request))
#     return render(request, "polls/index.html", context)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be pusblished in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

# def detail(request, qid):
#     question = get_object_or_404(Question, pk=qid)
#     # try:
#     #     question = Question.objects.get(pk=qid)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})
#     # return HttpResponse("You're looking at question %s." % qid)
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

# def results(request, qid):
#     question = get_object_or_404(Question, pk=qid)
#     # response = "You're looking at the results of question %s."
#     return render(request, "polls/results.html", {"question": question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, qid):
    # Small problem here. Function first gets the selected_choice object from the database,
    # then computes the new value of votes, and then saves it back to the database.
    # If two users of your website try to vote at exactly the same time,
    # this might go wrong: The same value, let’s say 42, will be retrieved for votes.
    # Then, for both users the new value of 43 is computed and saved,
    # but 44 would be the expected value. This is called a race condition. This is now fixed
    # F-function
    question = get_object_or_404(Question, pk=qid)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        # selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))