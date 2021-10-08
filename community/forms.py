from django.forms import ModelForm

from blood.models import Post
from community.models import Community, MakeRequest


class CommunityCreationForm(ModelForm):
    class Meta:
        model = Community
        exclude = ('creator', 'post', 'isapprove',)


class CommunityUpdateForm(ModelForm):
    class Meta:
        model = Community
        exclude = ('creator', 'post', 'isapprove',)


class MakeRequestForm(ModelForm):
    class Meta:
        model = MakeRequest
        fields = ("post",)

    def __init__(self, user, *args, **kwargs):
        super(MakeRequestForm, self).__init__(*args, **kwargs)
        self.fields['post'].queryset = Post.objects.filter(user=user)
