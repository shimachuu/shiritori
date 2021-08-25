from django.shortcuts import render
from django.views import generic
from .forms import TestGameForm

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "index.html"


def new_game(request):
    if request.method == "POST":
        form = TestGameForm(request.POST)
        
        #入力内容のチェック
        if form.is_valid():
            game = form.save(commit=False)
            game.player = request.user

            #スタート地点の尻文字を、1選択目に渡したい
            game.start_letter = game.start_station.last_letter

            #ゴール地点の頭文字をゲームIDに登録しておく（ゴール判定に使いたい
            game.goal_letter = game.goal_station.first_letter
            
            #start_dateは登録日時が自動入力
            
            game.save()

            #ゲームIDを渡して選択画面へ誘導
            #return redirect('select', var=game.pk)
    else:
        form = TestGameForm()

    return render(request, 'new_game.html', {'form': form})