from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    BLOOD_GROUP = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    NEED = [
        ('whole', 'Whole Blood'),
        ('platelets', 'Blood platelets'),
        ('plasma', 'Blood plasma')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=30, choices=BLOOD_GROUP, default='A+')
    need_type = models.CharField(max_length=30, choices=NEED, default='whole')
    amount = models.IntegerField()
    time = models.TimeField()
    date = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=264)
    short_note = models.TextField(max_length=264, blank=True)
    map_link = models.URLField(max_length=350)
    blood_managed = models.BooleanField(blank=True, default=False)
    urgent = models.BooleanField(blank=True, default=False)
    thana = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ['-date_created']


class Donation(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    bags = models.IntegerField()
    approve = models.BooleanField(blank=True, default=False)
