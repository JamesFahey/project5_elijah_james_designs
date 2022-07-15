from django.db import models

# Create your models here.


class Contact(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name