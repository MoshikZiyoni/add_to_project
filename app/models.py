from django.db import models

# Create your models here.
class AddAttraction(models.Model):
    city = models.TextField(max_length=100)
    name = models.TextField(max_length=500)
    latitude=models.FloatField(null=True)
    longitude=models.FloatField(null=True)
    photos=models.TextField(max_length=100)
    review_score=models.TextField(max_length=20,null=True)
    description=models.TextField(max_length=1000,null=True)
    website=models.TextField(max_length=100,null=True)
    real_price=models.TextField(max_length=200,null=True)
    hours=models.TextField(max_length=150,null=True)
    tel=models.TextField(max_length=100,null=True)
    address=models.TextField(max_length=100,null=True)
    tips=models.TextField(max_length=3000,null=True)
    