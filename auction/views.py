from django.shortcuts import render
from auction.auction_algo import auction_algo

def auction_list(request):
	li = auction_algo()
	return render(request,'auction/auction_list.html',{'auction_list':li})
