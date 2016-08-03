from django.contrib import admin
from auction.models import Mentor,Mentee,MenToMen_Rel

class MenAdmin(admin.ModelAdmin):
	list_display=['name']	

class MenToMen_RelAdmin(admin.ModelAdmin):
	list_display=['mentors','mentees']

admin.site.register(Mentor,MenAdmin)
admin.site.register(Mentee,MenAdmin)
admin.site.register(MenToMen_Rel,MenToMen_RelAdmin)
