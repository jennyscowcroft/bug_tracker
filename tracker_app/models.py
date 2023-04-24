from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from django.urls import reverse
from datetime import datetime

# Create your models here.

PRIORITY_CHOICES = (
    ("LOW", "LOW"),
    ("MED", "MEDIUM"),
    ("HI", "HIGH"),
)


class ProjectList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def get_absolute_url(self):
        return reverse("project", args=[self.id])

    def __str__(self):
        return self.title


class BugItem(models.Model):
    title = models.CharField(max_length=100)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="reporter")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="assignee")
    description = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    urgency = models.CharField(max_length= 10, default="LOW", choices=PRIORITY_CHOICES)
    project = models.ForeignKey(ProjectList, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse(
            "item-update", args=[str(self.project.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: urgency: {self.urgency}"
