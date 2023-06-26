
from django.db import models

class Action(models.Model):
    project_id = models.IntegerField()
    action_type = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

