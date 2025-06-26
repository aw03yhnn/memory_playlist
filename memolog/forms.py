from django import forms
from .models import Memory

# 記憶投稿用のフォームクラス
class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        # 投稿日時は自動設定されるので除外
        fields = ['title', 'description', 'song_title', 'artist_name', 'spotify_url']
        
        # フォームのラベルとプレースホルダーを設定
        labels = {
            'title': 'Memory Title',
            'description': 'Memory Description',
            'song_title': 'Song Title',
            'artist_name': 'Artist Name',
            'spotify_url': 'Spotify URL',
        }
        
        # 入力欄のプレースホルダーテキスト
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., High school graduation day',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Share your memory or story related to this song...',
                'class': 'form-control',
                'rows': 4
            }),
            'song_title': forms.TextInput(attrs={
                'placeholder': 'e.g., Bohemian Rhapsody',
                'class': 'form-control'
            }),
            'artist_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Queen',
                'class': 'form-control'
            }),
            'spotify_url': forms.URLInput(attrs={
                'placeholder': 'https://open.spotify.com/track/...',
                'class': 'form-control'
            }),
        } 