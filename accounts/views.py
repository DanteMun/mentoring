from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Profile
from .forms import MentorForm, MenteeForm, MentorUpdateForm, MenteeUpdateForm
#from mentoring.models import Mentoring

# Create your views here.
def signup_choice(request):
    return render(request, 'accounts/signup_choice.html')


#멘토 가입
def mentor_signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = MentorForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                authenticated_user = authenticate(username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'])
                login(request, authenticated_user)
                messages.success(request, '환영합니다. :)')
                return redirect('/')
        else:
            form = MentorForm()
        return render(request, 'accounts/mentor_signup.html', {'form': form,})
    else:
        messages.info(request, "이미 로그인되어있습니다. 로그아웃 이후 실행해주세요.")
        return redirect('index')


#멘티 가입
def mentee_signup(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            form = MenteeForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.save()
                authenticated_user = authenticate(username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'])
                login(request, authenticated_user)
                messages.info(request, '환영합니다. :)')
                return redirect('/')
        else:
            form = MenteeForm()
        return render(request, 'accounts/mentee_signup.html', {'form': form,})
    else:
        messages.info(request, "이미 로그인되어있습니다. 로그아웃 이후 실행해주세요.")
        return redirect('index')


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    profile = get_object_or_404(Profile, pk=request.user.profile.pk)
    mentoring_list = Mentoring.objects.all()
    mentoring_mine = []
    for mentoring in mentoring_list:
        if mentoring.author==request.user:
            mentoring_mine.append(mentoring)
        elif mentoring.acceptor==profile.phone:
            mentoring_mine.append(mentoring)
        else:
            pass
    if profile.is_mentor:
        return render(request, 'accounts/mentor_profile.html', {
            'user' : user,
            'profile' : profile,
            'mentoring_mine' : mentoring_mine,
            })
    else:
        return render(request, 'accounts/mentee_profile.html', {
            'user' : user,
            'profile' : profile,
            'mentoring_mine' : mentoring_mine,
            })


def profile_edit(request):
    user = get_object_or_404(User, pk=request.user.pk)
    if user.profile.is_mentor:
        if request.method == 'POST' :
            form = MentorUpdateForm(request.POST, instance = user.profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = MentorUpdateForm(instance=user.profile)
        return render(request, 'accounts/mentor_signup_edit.html', {'user': user, 'form': form, })
    else:
        if request.method == 'POST':
            form = MenteeUpdateForm(request.POST, instance=user.profile)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = MenteeUpdateForm(instance=user.profile)
        return render(request, 'accounts/mentee_signup_edit.html', {'user': user, 'form': form, })


def access_terms(request):
    return render(request, 'accounts/access_terms.html')


def personal_info_terms(request):
    return render(request, 'accounts/personal_info_terms.html')
