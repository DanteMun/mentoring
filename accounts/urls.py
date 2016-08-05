from django.conf.urls import url, include
from django.contrib.auth.views import login, logout
from django.conf import settings

from . import views
from .forms import LoginForm

urlpatterns = [
    url(r'^signupchoice/$', views.signup_choice, name='signup_choice'),
    url(r'^mentor_signup/$', views.mentor_signup, name='mentor_signup'),
    url(r'^mentee_signup/$', views.mentee_signup, name='mentee_signup'),
    url(r'^mentor_list/$', views.mentor_list, name='mentor_list'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^login/$', login, kwargs={'authentication_form': LoginForm, }, name='login'),
    url(r'', include('django.contrib.auth.urls')),
]