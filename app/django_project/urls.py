from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django_app.views import first_page

urlpatterns = [
    path("", first_page, name="django_app"),
    path("admin/", admin.site.urls),
    # path("", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
