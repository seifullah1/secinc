from rest_framework.permissions import BasePermission

def in_group(user, name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=name).exists()

class IncidentPermission(BasePermission):
    """
    admin/analyst: полный доступ
    reporter: CRUD только своих инцидентов
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        u = request.user
        if u.is_superuser or in_group(u, "admin") or in_group(u, "analyst"):
            return True
        return obj.reporter_id == u.id
