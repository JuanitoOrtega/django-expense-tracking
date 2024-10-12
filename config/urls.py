from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('incomes/', include('apps.incomes.urls')),
    path('authentication/', include('apps.authentication.urls')),
    path('preferences/', include('apps.userpreferences.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
