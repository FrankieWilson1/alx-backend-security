from django.db import models

class RequestLog(models.Model):
    """
    Model to log incoming requests.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Request from {self.ip_address} at\
            {self.timestamp} for {self.path}"
