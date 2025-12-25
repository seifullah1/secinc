from django.contrib import admin
from .models import Incident, SecurityEvent

@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "severity", "status", "asset", "reporter", "assignee", "created_at", "closed_at")
    list_filter = ("category", "severity", "status", "asset")
    search_fields = ("title", "description", "asset")
    autocomplete_fields = ("reporter", "assignee")
    ordering = ("-created_at",)
@admin.register(SecurityEvent)
class SecurityEventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_type", "username", "user", "ip_address", "is_admin_panel", "created_at")
    list_filter = ("event_type", "is_admin_panel", "created_at")
    search_fields = ("username", "ip_address", "path", "user_agent")
    ordering = ("-created_at",)