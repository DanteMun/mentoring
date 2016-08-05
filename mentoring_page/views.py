from django.shortcuts import render

def index(request):
    return render(request, 'mentoring_page/index.html')