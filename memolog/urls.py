from django.urls import path
from . import views

# URLパターンの名前空間を設定（他のアプリと重複を避けるため）
app_name = 'memolog'

# URLパターンの定義
urlpatterns = [
    path('', views.memory_list, name='memory_list'),
    path('memory/<int:memory_id>/', views.memory_detail, name='memory_detail'),
    path('memory/create/', views.memory_create, name='memory_create'),
    path('random/', views.random_memory, name='random_memory'),
    path('charts/', views.weekly_charts, name='weekly_charts'),
    path('api/spotify-recommendations/', views.get_spotify_recommendations, name='spotify_recommendations'),
] 