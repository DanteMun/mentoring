from auction.models import MenToMen_Rel

def auction_algo():
	mentor_id = 1
	mentee_num = 3
	li = list(MenToMen_Rel.objects.filter(mentors=mentor_id).values())
	li_sorted = sorted(sorted(li,key=lambda li:li["time"]),key=lambda li:li["price"],reverse=True)
	li_ranked = li_sorted[:mentee_num]
	return li_ranked