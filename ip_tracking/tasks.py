from celery import shared_task
from django.db.models import Count, Q
from django.utils import timezone
from .models import RequestLog, SuspiciousIP
import datetime

@shared_task
def detect_anomalies():
    """
    Detects and flags suspicious IPs based on request frequency and path access.
    """
    one_hour_ago = timezone.now() - datetime.timedelta(hours=1)
    
    # 1. Flag IPs with a high number of requests
    high_request_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('ip_address')
    ).filter(
        request_count__gt=100
    )

    for entry in high_request_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f"High request volume: \
                {entry['request_count']} requests in the last hour"}
        )

    # 2. Flag IPs accessing sensitive paths
    sensitive_paths = ['/admin/', '/login/']
    sensitive_access_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).filter(
        Q(path__in=sensitive_paths)
    ).values('ip_address').distinct()

    for entry in sensitive_access_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': "Accessed sensitive paths in the last hour"}
        )

    print("Anomaly detection task completed.")
