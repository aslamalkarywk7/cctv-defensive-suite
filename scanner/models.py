from django.db import models

class ScanResult(models.Model):
    host = models.CharField(max_length=255)
    port = models.CharField(max_length=10)
    protocol = models.CharField(max_length=10)
    method = models.CharField(max_length=50) # Exploit name or 'Brute Force'
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    device_info = models.TextField(blank=True, null=True)
    snapshot = models.TextField(blank=True, null=True) # Base64 Image data
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.host}:{self.port} - {self.method}"
