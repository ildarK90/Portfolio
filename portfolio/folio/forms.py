from django.forms import ModelForm
from .models import Skills


class TodoForm(ModelForm):
    class Meta:
        model = Skills
        fields = ['title', 'memo', 'important']