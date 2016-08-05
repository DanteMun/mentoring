from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'mentoring_page.views.index', name='index'),
]