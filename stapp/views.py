from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.views import generic
from .models import Prefecture, MstTestStation, TestGame, TestChoice
from .forms import TestGameForm, TestChoiceForm

from django.http import HttpResponse

from django.views.generic import CreateView, TemplateView

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class GoalView(TemplateView):
    template_name = "goal.html"



# new_gameもFormViewで書き換えられると思う
# render(url)での変数受け渡しを脱する必要がある
def new_game(request):

    if request.method == "POST":
        form = TestGameForm(request.POST) 
        
        # 入力内容のチェック
        if form.is_valid():
            game = form.save(commit=False) # 仮登録
            game.player = request.user

            # スタート地点の尻文字を、1選択目に渡したい
            game.start_letter = game.start_station.last_letter

            # ゴール地点の頭文字をゲームIDに登録しておく（ゴール判定に使いたいな）
            game.goal_letter = game.goal_station.first_letter

            # start_dateは登録日時が自動入力

            # DBに保存
            game.save()

            # 最初の駅選択に必要な情報を変数（dictionary型）にまとめ、url連結用に変換
            params = urlencode({
                'game': game.pk,
                'start_letter': game.start_letter,
                'goal_letter': game.goal_letter,
            })

            # 選択画面(urlのname='new_choice')のパスを取得
            redirect_url = reverse('stapp:new_choice')

            #ゲームIDを渡して選択画面へ移動＝'views.new_choice'を呼び出す
            url = f'{redirect_url}?{params}' # 'f'について　https://note.nkmk.me/python-f-strings/
            return redirect(url)
    else: # ← methodが'POST'ではない = 最初のページ表示時の処理
        form = TestGameForm()
    return render(request, 'new_game.html', {'form': form})



'''
memo: FormViewの処理の流れ（CreateViewもほぼ同じ）

    流れ（HTTP GET）
        as_view()で呼ばれて、HTTP methodがGETの場合、ProcessFormViewのdef getが呼ばれる
        FormMixin中のget_context_data()が呼ばれ、インスタンス変数のform_classがkwargs['form']に格納される
        今までと同様、templateをreturnする
    流れ（HTTP POST）
        as_view()で呼ばれて、HTTP methodがPOSTの場合、ProcessFormViewのdef postが呼ばれる
        FormMixinのget_form()が呼ばれ、値の挿入されたformを入手
        form.is_valid()でform classで定義されたvalidationの判定
        validであればFormMixinのform_valid(form)が呼ばれ, インスタンス変数のsuccess_urlにリダイレクトされる
        invlidであればエラーと一緒にGETにリダイレクトされる

'''


# レコードの新規作成は、文字通りCreateViewを使おう
# 21/8/28 createviewにしたことで、保存はできた→変数の受け取りなどどうするか
# 21/8/29 form使用を復活してフィルターと保存,変数を渡すのに成功！！！！！
class NewChoice(CreateView):

    form_class = TestChoiceForm    # forms.pyの呼び出したいformを指定
    template_name = 'new_choice.html'  # 表示するtemplate



    # 1.new_gameもしくは前のchoiceから変数('game','start_letter')を受け取る
    # 2.受け取った変数を反映させたformを表示する
    # form に kwargs を渡す関数
    def get_form_kwargs(self):
        kwargs = super(NewChoice, self).get_form_kwargs() # 継承。ようわからん
        
        # 独自で変数を追加する
        kwargs['game'] = self.request.GET.get('game')
        kwargs['start_letter'] = self.request.GET.get('start_letter')

        return kwargs



    # 選択後に飛ぶurlを作る関数
    def get_success_url(self):
        
        # 選択を変数に格納
        chosen_station = MstTestStation.objects.get(pk=self.request.POST.get('station'))
        game = TestGame.objects.get(pk=self.request.POST.get('game'))

        # 選択駅がゴール駅だったらゴールのページに飛ぶ
        if chosen_station == game.goal_station:
            url = reverse('stapp:goal')
        else:
            params = urlencode({
                'game': self.request.POST.get('game'),
                'start_letter': chosen_station.last_letter,
                })

            # 選択画面(urlのname='new_choice')のパスを取得
            redirect_url = reverse('stapp:new_choice')

            #ゲームIDを渡して選択画面へ移動＝'views.new_choice'を呼び出す
            url = f'{redirect_url}?{params}' # 'f'について　https://note.nkmk.me/python-f-strings/
            
        return url



    # ゴール判定は https://qiita.com/maisuto/items/33dfeb58f5953d1c5fdf の
    # 「投票処理」を参考にして実装しよう

# as_view()はViewに付属の関数。
# クロージャであるview(request, *args, **kwargs)関数を返す
new_choice = NewChoice.as_view()