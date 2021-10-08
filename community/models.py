from django.contrib.auth.models import User
from django.db import models
from blood.models import Post


class Community(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=35)
    banner = models.ImageField(upload_to='banner/')
    fb_group = models.URLField()
    isapprove = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MakeRequest(models.Model):
    community = models.ForeignKey(Community,
                                  on_delete=models.CASCADE,
                                  blank=True)

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True)

    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
