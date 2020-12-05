from functools import wraps
from random import sample, randint

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from recruiting.forms import RecruitForm
from recruiting.models import Answers, Question, Sith, Recruit
from copy import deepcopy


recruiting_list = 'recruiting:recruits_list'

def main(request):
    return render(request, 'recruiting/main.html')


def recruit(request):
    if request.method == 'POST':
        form = RecruitForm(request.POST)
        if form.is_valid():
            recruit = form.save()
            request.session['recruit_id'] = recruit.id
            return HttpResponseRedirect(reverse('recruiting:pass_test'))
    else:
        if 'sith_id' in request.session:
            del request.session['sith_id']
        form = RecruitForm()
    return render(request, 'recruiting/recruit.html', {'form': form})


def sith(request):
    if request.method == "POST":
        request.session['sith_id'] = int(request.POST['selected_sith'][0])
        return HttpResponseRedirect(reverse(recruiting_list))
    else:
        if 'recruit_id' in request.session:
            del request.session['recruit_id']
        siths = Sith.objects.all()
    return render(request, 'recruiting/sith.html', {'siths': siths})


def sith_select_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not 'sith_id' in request.session:
            return HttpResponseRedirect(reverse('recruiting:sith'))
        else:
            return function(request, *args, **kwargs)

    return wrap


@sith_select_required
def recruits_list(request):
    recruits = Recruit.objects.filter(sith=None).exclude(recruit_answers=None)
    return render(request, 'recruiting/recruits_list.html', {'recruits': recruits})


def sith_select_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not 'sith_id' in request.session:
            return HttpResponseRedirect(reverse('recruiting:sith'))
        else:
            return function(request, *args, **kwargs)

    return wrap


def recruit_should_not_be_accepted(function):
    @wraps(function)
    def wrap(request, recruit_id, *args, **kwargs):
        if Recruit.objects.get(id=recruit_id).sith is None:
            return function(request, recruit_id, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse(recruiting_list))

    return wrap


@sith_select_required
@recruit_should_not_be_accepted
def recruit_answers(request, recruit_id):
    if request.method == 'POST':
        recruit = Recruit.objects.get(id=recruit_id)
        recruit.sith_id = request.session['sith_id']
        recruit.save()
        send_mail('Принятие в орден ситхов',
                  'Вы назначены Рукой Тени к %s с %s.' % (recruit.sith.name, recruit.sith.planet),
                  'test_task_test10@mail.ru', [recruit.email])
        return HttpResponseRedirect(reverse(recruiting_list))
    else:
        answers = Answers.objects.filter(recruit_id=recruit_id)
        sith = Sith.objects.get(id=request.session['sith_id'])
        has_three_hands = True if sith.shadow_hands.count() >= 3 else False
    return render(request, 'recruiting/recruit_answers.html',
                  {'answers': answers, 'three_hands': has_three_hands})


def recruit_not_added_or_test_passed(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not 'recruit_id' in request.session:
            return HttpResponseRedirect(reverse('recruiting:recruit'))
        elif Answers.objects.filter(recruit_id=request.session['recruit_id']):
            return render(request, 'recruiting/ok.html')
        else:
            return function(request, *args, **kwargs)

    return wrap


@recruit_not_added_or_test_passed
def pass_test(request):
    if request.method == 'POST':
        post_data = deepcopy(dict(request.POST))
        del post_data['csrfmiddlewaretoken']
        for question_id, answer in post_data.items():
            Answers.objects.create(recruit_id=request.session['recruit_id'],
                                   question_id=int(question_id), answer=eval(answer[0]))
        response = render(request, 'recruiting/ok.html')
    else:
        questions = Question.objects.all()
#         random_questions = sample(list(questions), randint(1, len(questions)))
        response = render(request, 'recruiting/questions.html', {'questions': questions})
    return response


def additional(request):
    all_siths = Sith.objects.all()
    siths_one_more_hands = [sith for sith in all_siths if sith.shadow_hands.count() > 1]
    return render(request, 'recruiting/additional.html',
                  {'all_siths': all_siths, 'siths_one_more_hands': siths_one_more_hands})
