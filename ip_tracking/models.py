from django.db import models


class RequestLog(models.Model):
    """
    Model to log incoming requests.

    Arguments:
        ip_address (str): The IP address of the requester.
        timestamp (datetime): The time the request was received.
        path (str): The requested path.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Request from {self.ip_address} ({self.city}, {self.country})\
            at {self.timestamp} for {self.path}"


class BlockedIP(models.Model):
    """
    Model to log blocked IP addresses.

    Arguments:
        ip_address (str): The IP address that was blocked.
        reason (str): The reason for blocking the IP address.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blocked IP: {self.ip_address} at {self.timestamp}"


class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suspicious IP: {self.ip_address} ({self.reason})"
