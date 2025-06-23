from django.contrib import admin
from .models import Memory

# Register your models here.

# 管理画面でMemoryモデルを使えるように登録
@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    # 一覧画面で表示する項目（タイトル、曲名、アーティスト、投稿日時）
    list_display = ('title', 'song_title', 'artist_name', 'created_at')
    # 投稿日時でフィルタリングできるようにする
    list_filter = ('created_at',)
    # 検索できる項目（タイトル、説明、曲名、アーティスト名）
    search_fields = ('title', 'description', 'song_title', 'artist_name')
    # 編集不可の項目（投稿日時は自動設定されるため）
    readonly_fields = ('created_at',)
