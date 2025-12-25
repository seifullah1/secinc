from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Incident, SecurityEvent

@login_required
def dashboard(request):
    total_incidents = Incident.objects.count()
    open_incidents = Incident.objects.filter(status__in=[Incident.Status.NEW, Incident.Status.IN_PROGRESS]).count()
    total_events = SecurityEvent.objects.count()
    failed_events = SecurityEvent.objects.filter(event_type=SecurityEvent.EventType.LOGIN_FAILED).count()

    return render(request, "dashboard.html", {
        "total_incidents": total_incidents,
        "open_incidents": open_incidents,
        "total_events": total_events,
        "failed_events": failed_events,
    })

@login_required
def incidents_page(request):
    items = Incident.objects.select_related("reporter", "assignee").order_by("-created_at")[:200]
    return render(request, "incidents.html", {"items": items})

@login_required
def events_page(request):
    items = SecurityEvent.objects.order_by("-created_at")[:300]
    return render(request, "events.html", {"items": items})
@login_required
def reports_page(request):
    return render(request, "reports.html")