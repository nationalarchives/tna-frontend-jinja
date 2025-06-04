from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    path("healthcheck/", include("test.django.healthcheck.urls")),
    path("forms/kitchen-sink/", views.get_name),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
