import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API認証情報（本番環境では環境変数から取得）
SPOTIFY_CLIENT_ID = 'your_client_id_here'
SPOTIFY_CLIENT_SECRET = 'your_client_secret_here'

def extract_track_id_from_url(spotify_url):
    """
    Spotify URLからトラックIDを抽出する
    """
    # 正規表現でトラックIDを抽出
    pattern = r'spotify\.com/track/([a-zA-Z0-9]+)'
    match = re.search(pattern, spotify_url)
    if match:
        return match.group(1)
    return None

def get_spotify_track_info(spotify_url):
    """
    Spotify URLから曲名とアーティスト名を取得する
    """
    try:
        # トラックIDを抽出
        track_id = extract_track_id_from_url(spotify_url)
        if not track_id:
            return None, None
        
        # Spotify APIクライアントを作成
        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # トラック情報を取得
        track = sp.track(track_id)
        
        # 曲名とアーティスト名を抽出
        song_title = track['name']
        artist_name = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
        
        return song_title, artist_name
        
    except Exception as e:
        print(f"Error getting Spotify track info: {e}")
        return None, None 