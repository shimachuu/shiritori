from django.urls import path

from . import views


app_name = 'stapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('game/new/', views.new_game, name='new_game'),
    # path('game/select/', views.choice, name='choice')
]