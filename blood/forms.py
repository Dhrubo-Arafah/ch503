from django.forms import ModelForm

from blood.models import Post, Donation


class SeekingPost(ModelForm):
    class Meta:
        model = Post
        exclude = ['user', ]

class ResponseForm(ModelForm):
    class Meta:
        model=Donation
        fields=['bags',]