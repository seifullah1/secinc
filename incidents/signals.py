from datetime import timedelta
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from django.db.models import Q

from .models import SecurityEvent, Incident

def _get_ip(request):
    if not request:
        return ""
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")

def _get_ua(request):
    if not request:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")

def _is_admin_path(request):
    if not request:
        return False
    return (request.path or "").startswith("/admin")

def _path(request):
    if not request:
        return ""
    return request.path or ""

@receiver(user_logged_in)
def on_login_success(sender, request, user, **kwargs):
    SecurityEvent.objects.create(
        event_type=SecurityEvent.EventType.LOGIN_SUCCESS,
        username=getattr(user, "username", "") or "",
        user=user,
        ip_address=_get_ip(request),
        user_agent=_get_ua(request),
        path=_path(request),
        is_admin_panel=_is_admin_path(request),
    )

@receiver(user_login_failed)
def on_login_failed(sender, credentials, request, **kwargs):
    username = (credentials or {}).get("username", "") or ""
    ip = _get_ip(request)
    is_admin = _is_admin_path(request)

    SecurityEvent.objects.create(
        event_type=SecurityEvent.EventType.LOGIN_FAILED,
        username=username,
        user=None,
        ip_address=ip,
        user_agent=_get_ua(request),
        path=_path(request),
        is_admin_panel=is_admin,
    )
    window = timezone.now() - timedelta(minutes=10)
    fails_qs = SecurityEvent.objects.filter(
        event_type=SecurityEvent.EventType.LOGIN_FAILED,
        created_at__gte=window,
    ).filter(
        Q(username=username) | Q(ip_address=ip)
    )

    if fails_qs.count() >= 5:
        recent_incident_window = timezone.now() - timedelta(minutes=30)

        exists = Incident.objects.filter(
            category=Incident.Category.UNAUTHORIZED,
            status__in=[Incident.Status.NEW, Incident.Status.IN_PROGRESS],
            created_at__gte=recent_incident_window,
            description__icontains=username if username else "",
        ).exists()

        if not exists:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            reporter = User.objects.filter(is_superuser=True).order_by("id").first() or User.objects.order_by("id").first()

            if reporter:
                with transaction.atomic():
                    Incident.objects.create(
                        title="Suspicious login attempts (possible brute force)",
                        description=f"Auto-detected: >=5 failed logins in 10 minutes. username='{username}', ip='{ip}', admin_panel={is_admin}",
                        category=Incident.Category.UNAUTHORIZED,
                        severity=Incident.Severity.HIGH,
                        status=Incident.Status.NEW,
                        asset="Django Admin" if is_admin else "Auth",
                        detected_at=timezone.now(),
                        reporter=reporter,
                        assignee=None,
                    )
