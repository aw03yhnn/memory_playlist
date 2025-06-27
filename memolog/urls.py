from django.urls import path
from . import views

# URLパターンの名前空間を設定（他のアプリと重複を避けるため）
app_name = 'memolog'

# URLパターンの定義
urlpatterns = [
    # 記憶の一覧ページ（例：/memories/）
    path('', views.memory_list, name='memory_list'),
    # 新しい記憶を投稿するページ（例：/memories/create/）
    path('create/', views.memory_create, name='memory_create'),
    # ランダムな記憶を表示するページ（例：/memories/random/）
    path('random/', views.memory_random, name='memory_random'),
    # 個別の記憶の詳細ページ（例：/memories/1/）
    path('<int:pk>/', views.memory_detail, name='memory_detail'),
] 