from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

#都道府県テーブルはこれで確定。
#テーブル名MstPrefecture,属性はcdとnameで作り直すのもあり
#pkを自動生成されるidにしたくないければ明示が必要！
class Prefecture(models.Model):
    prf_no = models.IntegerField(default=0, unique=True, primary_key=True)
    prf_name = models.CharField(max_length=10)

    def __str__(self):
        return self.prf_name

#テスト用なのでガンガンいじっていこう
class MstTestStation(models.Model):
    no = models.IntegerField()
    name_kanji = models.CharField(max_length=100)
    name_hira = models.CharField(max_length=100)
    name_kata = models.CharField(max_length=100)
    first_letter = models.CharField(max_length=1)
    last_letter = models.CharField(max_length=1)
    is_ends_n = models.BooleanField()
    #ForeignKeyのon_deleteについて https://qiita.com/AJIKING/items/7448a6ad3cc2347ae4d5
    #都道府県テーブルを参照する駅名がある場合に、都道府県を削除できないようにする
    prf_no = models.ForeignKey(Prefecture, to_field='prf_no', on_delete=models.PROTECT)
    city_name = models.CharField(max_length=100)
    jr_co_name = models.CharField(max_length=100)
    rail_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name_kanji + '（' + self.name_hira + '）'

class TestGame(models.Model):
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_station = models.ForeignKey(MstTestStation, on_delete=models.PROTECT, related_name='start_staion')
    start_letter = models.CharField(max_length=1)
    goal_station = models.ForeignKey(MstTestStation, on_delete=models.PROTECT, related_name='goal_staion')
    goal_letter = models.CharField(max_length=1)
    start_date = models.DateTimeField(default=timezone.now)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return 'from ' + self.start_station.name_kata + ' to ' + self.goal_station.name_kata

class TestChoice(models.Model):
    game = models.ForeignKey(TestGame, on_delete=models.CASCADE)
    station = models.ForeignKey(MstTestStation, on_delete=models.CASCADE)

    def __str__(self):
        return self.station.name_kata