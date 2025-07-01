import requests
from datetime import datetime, timedelta
import json

# Last.fm API設定（本番環境では環境変数から取得）
LASTFM_API_KEY = 'your_lastfm_api_key_here'
LASTFM_BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

def get_weekly_chart(date):
    """
    指定された日付の週間チャートを取得する
    """
    try:
        # 日付から週の開始日（月曜日）を計算
        week_start = date - timedelta(days=date.weekday())
        
        # Last.fm APIパラメータ
        params = {
            'method': 'chart.getTopTracks',
            'api_key': LASTFM_API_KEY,
            'format': 'json',
            'limit': 10  # 上位10曲を取得
        }
        
        # APIリクエスト
        response = requests.get(LASTFM_BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # チャートデータを抽出
        tracks = []
        if 'tracks' in data and 'track' in data['tracks']:
            for track in data['tracks']['track']:
                tracks.append({
                    'title': track['name'],
                    'artist': track['artist']['name'],
                    'playcount': track['playcount']
                })
        
        return tracks
        
    except Exception as e:
        print(f"Error getting Last.fm chart: {e}")
        return []

def get_weekly_chart_for_memory(memory_date):
    """
    記憶の投稿日付に基づいて週間チャートを取得する
    """
    # 投稿日付をdatetimeオブジェクトに変換
    if isinstance(memory_date, str):
        memory_date = datetime.strptime(memory_date, '%Y-%m-%d')
    
    # 週間チャートを取得
    chart_tracks = get_weekly_chart(memory_date)
    
    return chart_tracks

def format_chart_for_display(chart_tracks):
    """
    チャートデータを表示用にフォーマットする
    """
    if not chart_tracks:
        return []
    
    formatted_tracks = []
    for i, track in enumerate(chart_tracks[:5], 1):  # 上位5曲のみ表示
        formatted_tracks.append({
            'rank': i,
            'title': track['title'],
            'artist': track['artist'],
            'playcount': track['playcount']
        })
    
    return formatted_tracks 