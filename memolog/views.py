from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Memory
from .forms import MemoryForm
from .lastfm_charts import get_weekly_charts
from .spotify_recommendations import get_track_recommendations, get_artist_top_tracks
import json

# Create your views here.

def memory_list(request):
    """記憶一覧を表示"""
    memories = Memory.objects.all().order_by('-created_at')
    return render(request, 'memolog/memory_list.html', {'memories': memories})

def memory_detail(request, memory_id):
    """記憶詳細を表示"""
    memory = get_object_or_404(Memory, pk=memory_id)
    
    # Spotify推薦曲を取得
    recommendations = []
    artist_tracks = []
    
    if memory.spotify_url:
        try:
            recommendations = get_track_recommendations(memory.spotify_url, limit=5)
            artist_tracks = get_artist_top_tracks(memory.spotify_url, limit=5)
        except Exception as e:
            print(f"Error getting recommendations: {e}")
    
    context = {
        'memory': memory,
        'recommendations': recommendations,
        'artist_tracks': artist_tracks
    }
    return render(request, 'memolog/memory_detail.html', context)

def memory_create(request):
    """記憶投稿フォームを表示・処理"""
    if request.method == 'POST':
        form = MemoryForm(request.POST)
        if form.is_valid():
            memory = form.save()
            return redirect('memory_detail', memory_id=memory.id)
    else:
        form = MemoryForm()
    
    return render(request, 'memolog/memory_form.html', {'form': form})

def random_memory(request):
    """ランダムな記憶を表示"""
    import random
    memories = list(Memory.objects.all())
    if memories:
        random_memory = random.choice(memories)
        return redirect('memory_detail', memory_id=random_memory.id)
    return redirect('memory_list')

def weekly_charts(request):
    """週間チャートを表示"""
    charts = get_weekly_charts()
    return render(request, 'memolog/weekly_charts.html', {'charts': charts})

@csrf_exempt
def get_spotify_recommendations(request):
    """AJAX用のSpotify推薦API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            spotify_url = data.get('spotify_url')
            
            if not spotify_url:
                return JsonResponse({'error': 'Spotify URL is required'}, status=400)
            
            recommendations = get_track_recommendations(spotify_url, limit=10)
            return JsonResponse({'recommendations': recommendations})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST method required'}, status=405)
