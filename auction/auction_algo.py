from auction.models import MenToMen_Rel

def auction_algo():
	mentor_id = 1
	li = list(MenToMen_Rel.objects.filter(mentors=mentor_id).values())
#li.sort(key=lambda li:li["mentees_id"]),key=lambda li:li["price"],reverse=True
	li_sorted = sorted(sorted(li,key=lambda li:li["time"]),key=lambda li:li["price"],reverse=True)
	
	return li_sorted