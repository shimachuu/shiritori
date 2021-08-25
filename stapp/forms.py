from django import forms

from .models import TestGame


class TestGameForm(forms.ModelForm):

    class Meta:
        model = TestGame
        fields = ('start_station', 'goal_station',)