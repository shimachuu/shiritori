from django import forms

from .models import Prefecture, MstTestStation, TestGame, TestChoice


class TestGameForm(forms.ModelForm):
    
    class Meta:
        model = TestGame
        fields = ('start_station', 'goal_station',)


class TestChoiceForm(forms.ModelForm):

    class Meta:
        model = TestChoice
        fields = ('game','station')

    def __init__(self, game_id, start_letter, *args, **kwargs):
        
        # https://sleepless-se.net/2018/07/10/django%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E5%86%85%E3%81%AE%E9%96%A2%E9%80%A3%E3%83%86%E3%83%BC%E3%83%96%E3%81%AB%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC%E3%82%92%E3%81%8B%E3%81%91%E3%82%8B/
        # initメソッドを丸っと継承する（意味不明だがないと動かない）
        super().__init__(*args, **kwargs)
        
        # start_letter = kwargs.get("instance").start_letter
        # start_letter = kwargs.pop('start_letter')
        self.start_letter = start_letter # 成功！
        self.fields['game'].initial = game_id

        # https://codor.co.jp/django/about-filter
        self.fields['station'].queryset = MstTestStation.objects.filter(first_letter=start_letter)

    