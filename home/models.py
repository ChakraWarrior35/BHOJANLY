
from django.db import models

# Create your models here

class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=122)
    message = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=122)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    customer_name = models.CharField(max_length=122)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    order_details = models.TextField()
    delivery_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery to {self.customer_name} at {self.address}"


# User model for delivery partner registration
from django.utils import timezone

class DeliveryPartner(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
