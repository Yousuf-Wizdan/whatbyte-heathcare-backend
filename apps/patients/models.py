from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patients'
    )
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (Age: {self.age})"
    
    class Meta:
        ordering = ['-created_at']
