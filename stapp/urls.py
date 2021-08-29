from django.urls import path

from . import views


app_name = 'stapp'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('game/goal/', views.GoalView.as_view(), name='goal'),
    path('game/new/', views.new_game, name='new_game'),
    path('game/choice/', views.new_choice, name='new_choice'),
]