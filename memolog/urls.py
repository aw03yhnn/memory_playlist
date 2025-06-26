from django.urls import path
from . import views

# URLパターンの名前空間を設定（他のアプリと重複を避けるため）
app_name = 'memolog'

# URLパターンの定義
urlpatterns = [
    # 記憶の一覧ページ（例：/memories/）
    path('', views.memory_list, name='memory_list'),
    # 個別の記憶の詳細ページ（例：/memories/1/）
    path('<int:pk>/', views.memory_detail, name='memory_detail'),
] 