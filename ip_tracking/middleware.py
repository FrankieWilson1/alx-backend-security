from django.http import HttpResponseForbidden

from .models import RequestLog, BlockedIP

class IPTrackingMiddleware:
    """
    Middleware to track IP addresses of incoming requests.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Cache the list of blocked IPs for performance.
        self.blocked_ips = set(
            BlockedIP.objects.values_list('ip_address', flat=True)
        )

    def __call__(self, request):
        # Get the client's IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0].strip()
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Check if the IP is in blacklist
        if ip_address in self.blocked_ips:
            return HttpResponseForbidden("You are blocked.")
        
        location = request.ipinfo
        country = getattr(location, 'country', None)
        city = getattr(location, 'city', None)

        # Log the request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=request.path,
            country=country,
            city=city
        )

        response = self.get_response(request)
        return response
