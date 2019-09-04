from django.core.exceptions import ValidationError
from django.forms import ModelForm
from recruiting.models import Recruit


class RecruitForm(ModelForm):
    class Meta:
        model = Recruit
        exclude = ['sith']


