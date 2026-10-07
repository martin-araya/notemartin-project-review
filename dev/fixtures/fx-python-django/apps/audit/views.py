from django.http import HttpResponse

from .models import AuditLog


def export_audit_csv(request):
    """Vista interna (no accesible publicamente).

    Trampa E05: esta vista existe pero NO esta enlazada en urls.py del
    proyecto, solo desde el shell de admin via la action `export_csv`.
    """
    logs = AuditLog.objects.all()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="audit_logs.csv"'
    response.write("\n".join(str(log.id) for log in logs))
    return response