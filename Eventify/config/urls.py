from django.contrib import admin
from django.urls import path, include
from events.views import homepage
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", include("events.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("events/", include("events.urls")),
    path("", homepage, name="homepage"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
