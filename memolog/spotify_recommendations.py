import requests
import re
import os
from typing import List, Dict, Optional

# Spotify API設定（環境変数から取得）
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', 'your_spotify_client_id_here')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_spotify_client_secret_here')
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_BASE = 'https://api.spotify.com/v1'

def get_spotify_access_token():
    """
    Spotify APIのアクセストークンを取得する
    """
    try:
        # Client Credentials Flowを使用
        auth_response = requests.post(SPOTIFY_TOKEN_URL, {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        })
        
        auth_response.raise_for_status()
        auth_data = auth_response.json()
        return auth_data['access_token']
        
    except Exception as e:
        print(f"Error getting Spotify access token: {e}")
        return None

def extract_track_id_from_url(spotify_url: str) -> Optional[str]:
    """
    Spotify URLからトラックIDを抽出する
    """
    pattern = r'spotify\.com\/.*\/track\/([a-zA-Z0-9]+)'
    match = re.search(pattern, spotify_url)
    return match.group(1) if match else None

def get_track_recommendations(spotify_url: str, limit: int = 5) -> List[Dict]:
    """
    Spotify URLから関連曲を取得する
    """
    try:
        # トラックIDを抽出
        track_id = extract_track_id_from_url(spotify_url)
        if not track_id:
            return []
        
        # アクセストークンを取得
        access_token = get_spotify_access_token()
        if not access_token:
            return []
        
        # 関連曲を取得
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        params = {
            'seed_tracks': track_id,
            'limit': limit,
            'market': 'JP'  # 日本市場
        }
        
        response = requests.get(
            f'{SPOTIFY_API_BASE}/recommendations',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        
        # 推薦曲をフォーマット
        recommendations = []
        for track in data.get('tracks', []):
            recommendations.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                'spotify_url': track['external_urls']['spotify'],
                'album': track['album']['name'],
                'popularity': track['popularity']
            })
        
        return recommendations
        
    except Exception as e:
        print(f"Error getting Spotify recommendations: {e}")
        return []

def get_artist_top_tracks(spotify_url: str, limit: int = 5) -> List[Dict]:
    """
    アーティストの人気曲を取得する
    """
    try:
        # トラックIDを抽出
        track_id = extract_track_id_from_url(spotify_url)
        if not track_id:
            return []
        
        # アクセストークンを取得
        access_token = get_spotify_access_token()
        if not access_token:
            return []
        
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        
        # まずトラック情報を取得してアーティストIDを取得
        track_response = requests.get(
            f'{SPOTIFY_API_BASE}/tracks/{track_id}',
            headers=headers
        )
        track_response.raise_for_status()
        track_data = track_response.json()
        
        artist_id = track_data['artists'][0]['id']
        
        # アーティストの人気曲を取得
        artist_response = requests.get(
            f'{SPOTIFY_API_BASE}/artists/{artist_id}/top-tracks?market=JP',
            headers=headers
        )
        artist_response.raise_for_status()
        artist_data = artist_response.json()
        
        # 人気曲をフォーマット
        top_tracks = []
        for track in artist_data.get('tracks', [])[:limit]:
            top_tracks.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown Artist',
                'spotify_url': track['external_urls']['spotify'],
                'album': track['album']['name'],
                'popularity': track['popularity']
            })
        
        return top_tracks
        
    except Exception as e:
        print(f"Error getting artist top tracks: {e}")
        return [] 