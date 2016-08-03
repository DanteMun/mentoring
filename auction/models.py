from django.db import models
from django.utils import timezone

class Mentor(models.Model):
	name = models.CharField(max_length=20)
	mentees = models.ManyToManyField('Mentee',through = 'MenToMen_Rel')
	def __str__(self):
		return self.name

class Mentee(models.Model):
	name = models.CharField(max_length=20)
	def __str__(self):
		return self.name

class MenToMen_Rel(models.Model):
	mentors = models.ForeignKey(Mentor)
	mentees = models.ForeignKey(Mentee)
	price = models.IntegerField(default=0)
	time = models.DateTimeField(default=timezone.now)