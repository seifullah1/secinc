"""
URL configuration for secinc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from incidents.views import IncidentViewSet, export_incidents_excel, set_lang, set_theme
from incidents.web_views import dashboard, incidents_page, events_page, reports_page
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = DefaultRouter()
router.register("incidents", IncidentViewSet, basename="incidents")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("reports/", reports_page, name="reports_page"),
    path("reports/incidents.xlsx", export_incidents_excel),
    path("ui/theme/", set_theme, name="set_theme"),
    path("ui/lang/", set_lang, name="set_lang"),
    path("", dashboard, name="dashboard"),
    path("incidents/", incidents_page, name="incidents_page"),
    path("events/", events_page, name="events_page"),

    # auth pages
    path("accounts/", include("django.contrib.auth.urls")),

    # API
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
]