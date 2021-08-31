from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode
from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Prefecture, MstTestStation, TestGame, TestChoice
from .forms import TestChoiceForm, TestGameForm
from django.views.generic import CreateView, TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

@method_decorator(login_required, name='dispatch')
class GoalView(TemplateView):
    template_name = "goal.html"



# new_gameもFormViewで書き換えられると思う　→ 8/29 書き換えた
# render(url)での変数受け渡しを脱する必要がある

'''関数ベースver
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


# クラスベースビューに書き換え
# デコレータについて　https://programming.sincoston.com/django-classbaseview-decorator/
@method_decorator(login_required, name='dispatch')
class NewGame(CreateView):
    # model = TestGame
    # fields = ['start_station', 'goal_station']
    
    form_class = TestGameForm
    template_name = 'new_game.html'
    

    # templateに都道府県リストを渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parentcategory_list'] = Prefecture.objects.all()
        # context['station_list'] = MstTestStation.objects.filter(is_ends_n=False)
        return context


    # formに抜け漏れがなければ行う
    def form_valid(self, form):
        form.instance.player = self.request.user

        # スタート地点の尻文字を、1選択目に渡す
        # 'instance'がないとダメらしい
        form.instance.start_letter = form.instance.start_station.last_letter

        # ゴール地点の頭文字をゲームIDに登録しておく（ゴール判定に使う）
        form.instance.goal_letter = form.instance.goal_station.first_letter

        return super().form_valid(form)


    def get_success_url(self):
        # 最初の駅選択に必要な情報を変数（dictionary型）にまとめ、url連結用に変換
        params = urlencode({
            'game': self.object.pk,
            'start_letter': self.object.start_letter,
            'goal_letter': self.object.goal_letter,
        })

        # 選択画面(urlのname='new_choice')のパスを取得
        redirect_url = reverse('stapp:new_choice')

        #ゲームIDを渡して選択画面へ移動＝'views.new_choice'を呼び出す
        url = f'{redirect_url}?{params}' # 'f'について　https://note.nkmk.me/python-f-strings/
        
        return url

# as_view()はViewに付属の関数。
# クロージャであるview(request, *args, **kwargs)関数を返す
new_game = NewGame.as_view()


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
@method_decorator(login_required, name='dispatch')
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
        chosen_station = self.object.station
        game = self.object.game

        # 選択駅がゴール駅だったらゴールのページに飛ぶ
        # ゴール判定は https://qiita.com/maisuto/items/33dfeb58f5953d1c5fdf の
        # 「投票処理」を参考にして実装
        if chosen_station == game.goal_station:
            url = reverse('stapp:goal')
            # return resolve_url('polls:results', self.kwargs['pk'])
            # しりとりの軌跡を表示したい

            # is_finishedをtrueに書き換える
            game_finished = get_object_or_404(TestGame, pk=game.pk)
            game_finished.is_finished = True
            game_finished.save()
        else:
            params = urlencode({
                'game': game.pk,
                'start_letter': chosen_station.last_letter,
            })

            # 選択画面(urlのname='new_choice')のパスを取得
            redirect_url = reverse('stapp:new_choice')

            #ゲームIDを渡して選択画面へ移動＝'views.new_choice'を呼び出す
            url = f'{redirect_url}?{params}' # 'f'について　https://note.nkmk.me/python-f-strings/
            
        return url


    '''def goal(pk):
        game = get_object_or_404(TestGame, pk=pk)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
        game.is_finished = True
        game.save()
        #return reverse('stapp:goal')'''

new_choice = NewChoice.as_view()