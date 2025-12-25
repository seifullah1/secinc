from datetime import timedelta
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from .models import LoginLock

LOCK_THRESHOLD = 5
LOCK_MINUTES = 10
WINDOW_MINUTES = 10

class LockoutBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        u = (username or "")[:150]
        ip = ""
        if request:
            xff = request.META.get("HTTP_X_FORWARDED_FOR")
            ip = (xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", ""))
        lock = LoginLock.objects.filter(username=u, ip_address=ip).first()
        if lock and lock.is_locked():
            return None
        user = super().authenticate(request, username=username, password=password, **kwargs)

        now = timezone.now()
        if user is None:
            lock, _ = LoginLock.objects.get_or_create(username=u, ip_address=ip)
            if lock.window_started_at < now - timedelta(minutes=WINDOW_MINUTES):
                lock.failed_count = 0
                lock.window_started_at = now

            lock.failed_count += 1

            if lock.failed_count >= LOCK_THRESHOLD:
                lock.locked_until = now + timedelta(minutes=LOCK_MINUTES)

            lock.save()
            return None
        LoginLock.objects.filter(username=u, ip_address=ip).delete()
        return user
