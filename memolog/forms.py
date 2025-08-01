from django import forms
from .models import Memory
from .utils import get_spotify_track_info

class MemoryForm(forms.ModelForm):
    class Meta:
        model = Memory
        fields = ['title', 'description', 'song_title', 'artist_name', 'spotify_url']
        
        labels = {
            'title': 'Memory Title',
            'description': 'Memory Description',
            'song_title': 'Song Title',
            'artist_name': 'Artist Name',
            'spotify_url': 'Spotify URL',
        }
        
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
                'class': 'form-control',
                'id': 'song_title_field'
            }),
            'artist_name': forms.TextInput(attrs={
                'placeholder': 'e.g., Queen',
                'class': 'form-control',
                'id': 'artist_name_field'
            }),
            'spotify_url': forms.URLInput(attrs={
                'placeholder': 'https://open.spotify.com/track/...',
                'class': 'form-control',
                'id': 'spotify_url_field'
            }),
        }
    
    def clean(self):
        """フォームのバリデーション時にSpotify URLから曲情報を自動取得"""
        cleaned_data = super().clean()
        spotify_url = cleaned_data.get('spotify_url')
        
        if spotify_url:
            song_title, artist_name = get_spotify_track_info(spotify_url)
            
            if song_title and artist_name:
                cleaned_data['song_title'] = song_title
                cleaned_data['artist_name'] = artist_name
        
        return cleaned_data 