from django.db import models

class Databases(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, unique=True)  # Increased max_length
    message = models.TextField(max_length=500, blank=True, null=True)  # Allow blank and null

    def __str__(self):
        return self.name