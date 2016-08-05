from django.conf.urls import url, include
from django.contrib import admin
from auction import views as auction_views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^auction/$',auction_views.auction_list),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^mentoring/', include('mentoring_page.urls', namespace='mentoring')),
    url(r'^$', lambda request:redirect('/mentoring/')),
]




urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)