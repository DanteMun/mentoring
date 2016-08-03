from django.conf.urls import url
from django.contrib import admin
from auction import views as auction_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auction/$',auction_views.auction_list)
]
