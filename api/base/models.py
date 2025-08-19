from django.db import models

class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    done = models.BooleanField(default=False)
    tasks = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    clients = models.CharField(max_length=255, null=True, blank=True)
    entreprise = models.CharField(max_length=255, null=True, blank=True)
    tech_stack = models.CharField(max_length=255, null=True, blank=True)
    projects = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.projects} - {self.tasks}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
