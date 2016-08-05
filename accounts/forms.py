import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.conf import settings

from .models import Profile, MAJOR_CHOICES, ADMISSION_TYPE_CHOICES, GRADE_CHOICES, ACCESS_ROUTE
from .fields import RestrictedImageField

def phone_validator(value):
    number = ''.join(re.findall(r'\d+', value))
    return RegexValidator(r'^01[016789]\d{7,8}$', message='번호를 입력해주세요')(number)

class MentorForm(UserCreationForm):
    username = forms.CharField(label='아이디')
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    name = forms.CharField(label='이름')
    major = forms.ChoiceField(label='소속학과', choices=MAJOR_CHOICES)
    admission_type = forms.ChoiceField(label='입학전형', choices=ADMISSION_TYPE_CHOICES)
    highschool = forms.CharField(label='출신고등학교')
    phone = forms.CharField(label='휴대폰 번호', widget=forms.TextInput(attrs={'placeholder': 'ex) 010-1234-5678'}), validators=[phone_validator])
    image = RestrictedImageField(max_upload_size=3145728, label='프로필 사진')
    intro = forms.CharField(label='각종 약력', widget=forms.TextInput(attrs={'placeholder': '멘토링,과외 경험, 각종 대회 수상, 인증시험 등'}))

    #is_agree = forms.BooleanField(label='약관동의', error_messages={
        #'required' : '약관동의를 해주셔야 가입이 됩니다.',
    #})

    error_messages = {
        'password_mismatch': _("비밀번호가 일치하지 않습니다."),
    }

    widgets = {
        'major': forms.RadioSelect(attrs={'style':'display: none'}),
        'admission_type': forms.RadioSelect(attrs={'style':'display: none'}),
        }


    def save(self, commit=True):
        user = super(MentorForm, self).save(commit=False)
        if commit:
            user.save()
            user.profile.name = self.cleaned_data['name']
            user.profile.major = self.cleaned_data['major']
            user.profile.admission_type = self.cleaned_data['admission_type']
            user.profile.highschool = self.cleaned_data['highschool']
            user.profile.phone = self.cleaned_data['phone']
            user.profile.image = self.cleaned_data['image']
            user.profile.intro = self.cleaned_data['intro']
            user.profile.is_mentor = True
            user.profile.save()
        return user


class MentorUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'major', 'admission_type', 'highschool', 'phone', 'intro', )


class MenteeForm(UserCreationForm):
    username = forms.CharField(label='아이디')
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)
    name = forms.CharField(label='이름')
    #major = forms.ChoiceField(label='지망학과', choices=MAJOR_CHOICES)
    #admission_type = forms.ChoiceField(label='희망입시전형', choices=ADMISSION_TYPE_CHOICES)
    #phone = forms.CharField(label='휴대폰 번호', widget=forms.TextInput(attrs={'placeholder': 'ex) 010-1234-5678'}), validators=[phone_validator])
    grade = forms.ChoiceField(label='학년', choices=GRADE_CHOICES)
    access_route = forms.ChoiceField(label='가입경로', choices=ACCESS_ROUTE)
    #is_agree = forms.BooleanField(label='약관동의', error_messages={
    #    'required' : '약관동의를 해주셔야 가입이 됩니다.',
    #})

    error_messages = {
        'password_mismatch': _("비밀번호가 일치하지 않습니다."),
    }

    def save(self, commit=True):
        user = super(MenteeForm, self).save(commit=False)
        if commit:
            user.save()
            user.profile.name = self.cleaned_data['name']
            user.profile.grade = self.cleaned_data['grade']
            user.profile.access_route = self.cleaned_data['access_route']
            user.profile.is_mentor = False
            user.profile.save()
        return user


class MenteeUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'grade',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='아이디')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput())