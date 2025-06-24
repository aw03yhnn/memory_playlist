from django.db import models

# 記憶とSpotifyの曲を1セットで保存するモデル
class Memory(models.Model):
    # 記憶のタイトル（例：「高校の帰り道」）
    title = models.CharField(max_length=100, verbose_name='Title')
    # その記憶の詳細な内容や思い出
    description = models.TextField(verbose_name='Description')
    # その記憶に関連する曲のタイトル
    song_title = models.CharField(max_length=200, verbose_name='Song Title')
    # 曲のアーティスト名
    artist_name = models.CharField(max_length=200, verbose_name='Artist Name')
    # Spotifyの曲へのリンク
    spotify_url = models.URLField(verbose_name='Spotify URL')
    # 投稿された日時（自動で現在時刻が設定される）
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    
    # 管理画面での表示設定
    class Meta:
        verbose_name = 'Memory'
        verbose_name_plural = 'Memories'
        # 新しい投稿が上に表示されるように並び順を設定
        ordering = ['-created_at']
    
    # 管理画面でタイトルが表示されるように設定
    def __str__(self):
        return self.title