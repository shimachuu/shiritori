from django import forms

from .models import Prefecture, MstTestStation, TestGame, TestChoice

# createviewの機能でまかなうことにしたので、下記フォームはいったんコメントアウト
# 21/8/30 県名（親カテゴリ）で動的に絞り込むため復活
class TestGameForm(forms.ModelForm):
    
    start_prf = forms.ModelChoiceField(
        label = 'スタート都道府県',
        queryset = Prefecture.objects,
        required = False
    )

    goal_prf = forms.ModelChoiceField(
        label = 'ゴール都道府県',
        queryset = Prefecture.objects,
        required = False
    )


    class Meta:
        model = TestGame
        fields = ('start_prf','start_station','goal_prf', 'goal_station',)
        
        # widgetの種類　https://docs.djangoproject.com/en/3.2/ref/forms/widgets/#django.forms.SelectDateWidget
        '''widgets = {
            'start_station': forms.RadioSelect, 
            'goal_station': forms.RadioSelect,
        }'''



class TestChoiceForm(forms.ModelForm):

    class Meta:
        model = TestChoice
        fields = ('game','station')
        widgets = {
            'game': forms.HiddenInput,
        }

    # formが画面に表示される前に何をするかを定める
    def __init__(self, *args, **kwargs):
        # https://hideharaaws.hatenablog.com/entry/2017/02/05/021111
        self.start_letter = kwargs.pop('start_letter')
        self.game  = kwargs.pop('game')
        
        # https://sleepless-se.net/2018/07/10/django%E3%83%95%E3%82%A9%E3%83%BC%E3%83%A0%E5%86%85%E3%81%AE%E9%96%A2%E9%80%A3%E3%83%86%E3%83%BC%E3%83%96%E3%81%AB%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF%E3%83%BC%E3%82%92%E3%81%8B%E3%81%91%E3%82%8B/
        # ModelForm（親クラス）のinitメソッドを丸っと継承する（意味不明だがないと動かない）
        super().__init__(*args, **kwargs)
        
        # start_letter = kwargs.get("instance").start_letter
        # start_letter = kwargs.pop('start_letter')
        
        self.fields['game'].initial = self.game

        # https://codor.co.jp/django/about-filter
        self.fields['station'].queryset = MstTestStation.objects.filter(first_letter=self.start_letter)

        # super().__init__(*args, **kwargs)

    