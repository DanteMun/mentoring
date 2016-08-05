from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User

from mentoring.utils import thumbnail, random_name_upload_to



MAJOR_CHOICES = (
    ('간호대학', '간호대학'),
    ('건축학과', '건축학과'),
    ('경영대학', '경영대학'),
    ('농경제사회학부', '농경제사회학부'),
    ('사회과학계열', '사회과학계열'),
    ('심리학과', '심리학과'),
    ('소비자아동학부', '소비자아동학부'),
    ('의류학과', '의류학과'),
    ('인문계열', '인문계열'),
    ('언어학과', '언어학과'),
    ('교육학과', '교육학과'),
    ('국어교육과', '국어교육과'),
    ('물리교육과', '물리교육과'),
    ('사회교육과', '사회교육과'),
    ('생물교육과', '생물교육과'),
    ('역사교육과', '역사교육과'),
    ('영어교육과', '영어교육과'),
    ('지구과학교육과', '지구과학교육과'),
    ('지리교육과', '지리교육과'),
    ('체육교육과', '체육교육과'),
    ('화학교육과', '화학교육과'),
    ('수학교육과', '수학교육과'),
    ('물리천문학부', '물리천문학부'),
    ('바이오시스템소재학부', '바이오시스템소재학'),
    ('산림과학부', '산림과학부'),
    ('생명과학부', '생명과학부'),
    ('수리과학부', '수리과학부'),
    ('식물생산과학부', '식물생산과학부'),
    ('식품영양학과', '식품영양학과'),
    ('응용생물화학부', '응용생물화학부'),
    ('화학부', '화학부'),
    ('건설환경공학부', '건설환경공학부'),
    ('기계항공공학부', '기계항공공학부'),
    ('산업공학과', '산업공학과'),
    ('식품동물생명공학부', '식품동물생명공학부'),
    ('재료공학부', '재료공학부'),
    ('전기정보공학부', '전기정보공학부'),
    ('조경지역시스템공학부', '조경지역시스템공학부'),
    ('조선해양공학과', '조선해양공학과'),
    ('컴퓨터공학부', '컴퓨터공학부'),
    ('화학생물공학부', '화학생물공학부'),
    ('의예과', '의예과'),

)

ADMISSION_TYPE_CHOICES = (
    ('지역균형선발전형', '지역균형선발전형'),
    ('일반전형(특기자)', '일반전형(특기자)'),
    ('기회균형선발특별전형', '기회균형선발특별전형'),
    ('정시전형', '정시전형'),

)

GRADE_CHOICES = (
    ('초등학교 1학년', '초등학교 1학년'),
    ('초등학교 2학년', '초등학교 2학년'),
    ('초등학교 3학년', '초등학교 3학년'),
    ('초등학교 4학년', '초등학교 4학년'),
    ('초등학교 5학년', '초등학교 5학년'),
    ('초등학교 6학년', '초등학교 6학년'),
    ('중학교 1학년', '중학교 1학년'),
    ('중학교 2학년', '중학교 2학년'),
    ('중학교 3학년', '중학교 3학년'),
    ('고등학교 1학년', '고등학교 1학년'),
    ('고등학교 2학년', '고등학교 2학년'),
    ('고등학교 3학년', '고등학교 3학년'),
    ('N수생', 'N수생'),
)

ACCESS_ROUTE = (
    ('지인소개', '지인소개'),
    ('학원소개', '학원소개'),
    ('페이스북', '페이스북'),
    ('네이버', '네이버'),
    ('전단지', '전단지'),
    ('기타', '기타'),


)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, verbose_name='이름')
    #멘토 only
    major = models.CharField(max_length=40, choices=MAJOR_CHOICES, default='', verbose_name='전공', blank=True)
    phone = models.CharField(max_length=20, null=True, verbose_name='전화번호')
    admission_type = models.CharField(max_length=40, choices=ADMISSION_TYPE_CHOICES, default='', verbose_name='입학 전형')
    is_mentor = models.BooleanField(default=False)
    frequency = models.IntegerField(default=0)
    rating = models.FloatField(blank=True, default=0)
    highschool = models.CharField(blank=True, max_length=40, verbose_name='출신 고등학교')
    image = models.ImageField(blank=True, null=True, upload_to=random_name_upload_to, verbose_name='사진 업로드')
    intro = models.TextField(max_length=300, verbose_name='기타 약력')

    #멘티 only
    grade = models.CharField(max_length=20, verbose_name='학년')
    access_route = models.CharField(max_length=80, choices=ACCESS_ROUTE, verbose_name='가입경로')

    def __str__(self):

        if str(self.is_mentor) == "True":
            return "멘토 ||  "+self.name+" ( ID : "+self.user.username+" , 전화번호 : " + str(self.phone) + " )"
        else:
            return "멘티 ||  "+self.name+" ( ID : "+self.user.username+" )"

def pre_on_mentorimage_save(sender, **kwargs):
    mentor_image = kwargs['instance']
    if mentor_image.image:
        max_width = 800
        if mentor_image.image.width > max_width or mentor_image.image.height > max_width:
            processed_file = thumbnail(mentor_image.image.file, max_width, max_width)
            mentor_image.image.save(mentor_image.image.name, File(processed_file))

pre_save.connect(pre_on_mentorimage_save, sender=Profile)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()

post_save.connect(create_profile, sender=User)