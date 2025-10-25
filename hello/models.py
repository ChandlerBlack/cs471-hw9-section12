from django.db import models
import secrets

# Create your models here.


class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class RequestRecord(models.Model):
    """Stores each access timestamp and a randomly generated string (token)."""
    when = models.DateTimeField("date created", auto_now_add=True)
    token = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"{self.when.isoformat()} - {self.token}"
