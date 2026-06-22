from django.db import models
from accounts.models import CustomUser

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"