from django.db import models

# Create your models here.



# Class ContactUs creates a table for contact us page.

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
    

class SearchRecord(models.Model):
    username = models.CharField(max_length=255, default='admin')
    user_input = models.CharField(max_length=1255)
    response = models.CharField(max_length=5000)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.date_time}"