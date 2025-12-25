import csv
from django.http import HttpResponse
from django.db.models import Count, Avg, F, DurationField, ExpressionWrapper
from django.db.models.functions import TruncDate

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from openpyxl import Workbook
from django.http import HttpResponse
from .models import Incident
from .models import Incident
from .serializers import IncidentSerializer
from .permissions import IncidentPermission, in_group
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    permission_classes = [IncidentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "severity", "category", "asset", "assignee", "reporter"]
    search_fields = ["title", "description", "asset"]
    ordering_fields = ["created_at", "detected_at", "severity", "status"]

    def get_queryset(self):
        u = self.request.user
        qs = Incident.objects.select_related("reporter", "assignee").all()
        if u.is_superuser or in_group(u, "admin") or in_group(u, "analyst"):
            return qs
        return qs.filter(reporter=u)

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        inc = self.get_object()
        inc.close()
        inc.save(update_fields=["status", "closed_at"])
        return Response({"ok": True, "closed_at": inc.closed_at})

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        qs = self.get_queryset()

        by_status = list(qs.values("status").annotate(count=Count("id")).order_by("-count"))
        by_severity = list(qs.values("severity").annotate(count=Count("id")).order_by("-count"))
        by_category = list(qs.values("category").annotate(count=Count("id")).order_by("-count"))

        trend = list(
            qs.annotate(day=TruncDate("created_at"))
              .values("day")
              .annotate(count=Count("id"))
              .order_by("day")
        )

        closed = qs.filter(closed_at__isnull=False)
        duration = ExpressionWrapper(F("closed_at") - F("created_at"), output_field=DurationField())
        mttr = closed.annotate(d=duration).aggregate(avg=Avg("d"))["avg"]

        return Response({
            "by_status": by_status,
            "by_severity": by_severity,
            "by_category": by_category,
            "trend_by_day": trend,
            "mttr_avg": str(mttr) if mttr else None,
        })

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        qs = self.get_queryset().order_by("-created_at")

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="incidents.csv"'

        writer = csv.writer(response)
        writer.writerow(["id", "title", "category", "severity", "status", "asset", "reporter", "assignee", "created_at", "closed_at"])

        for i in qs:
            writer.writerow([
                i.id, i.title, i.category, i.severity, i.status, i.asset,
                i.reporter.username, (i.assignee.username if i.assignee else ""),
                i.created_at.isoformat(), (i.closed_at.isoformat() if i.closed_at else "")
            ])

        return response
@login_required
def export_incidents_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Инциденты"

    ws.append([
        "ID",
        "Название",
        "Категория",
        "Уровень",
        "Статус",
        "Актив",
        "Дата создания",
    ])

    for i in Incident.objects.all():
        ws.append([
            i.id,
            i.title,
            i.category,
            i.severity,
            i.status,
            i.asset,
            i.created_at.strftime("%d.%m.%Y %H:%M"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="incidents.xlsx"'
    wb.save(response)
    return response
@require_POST
def set_theme(request):
    theme = request.POST.get("theme", "dark")
    if theme not in ("dark", "light"):
        theme = "dark"
    resp = redirect(request.META.get("HTTP_REFERER", "/"))
    resp.set_cookie("theme", theme, max_age=60*60*24*365)  # 1 год
    return resp

@require_POST
def set_lang(request):
    lang = request.POST.get("lang", "ru")
    if lang not in ("ru", "kk"):
        lang = "ru"
    resp = redirect(request.META.get("HTTP_REFERER", "/"))
    resp.set_cookie("lang", lang, max_age=60*60*24*365)
    return resp