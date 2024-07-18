from django import forms
from dm.models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']