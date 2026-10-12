from django.db import models

# Create your models here.
class Endpoint(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    method = models.CharField(max_length=10,choices=[("GET","GET"),("POST","POST")])
    created_at = models.DateTimeField(auto_now_add=True)

class TestRun(models.Model):
    endpoint = models.ForeignKey(
        Endpoint,
        on_delete=models.CASCADE,
        related_name="test_runs"
    )
    status_code = models.IntegerField(null=True,blank=True)
    success = models.BooleanField(default=False)
    response_time_ms = models.FloatField()
    error_msg = models.TextField(blank=True,default="")
    created_at = models.DateTimeField(auto_now_add=True)