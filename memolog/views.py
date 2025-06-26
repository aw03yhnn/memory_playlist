from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Memory
from .forms import MemoryForm

# Create your views here.

# 記憶の一覧を表示するビュー
def memory_list(request):
    # 投稿日時の新しい順で記憶を取得
    memories = Memory.objects.all().order_by('-created_at')
    return render(request, 'memolog/memory_list.html', {'memories': memories})

# 個別の記憶の詳細を表示するビュー
def memory_detail(request, pk):
    # 指定されたIDの記憶を取得（存在しない場合は404エラー）
    memory = get_object_or_404(Memory, pk=pk)
    return render(request, 'memolog/memory_detail.html', {'memory': memory})

# 新しい記憶を投稿するビュー
def memory_create(request):
    if request.method == 'POST':
        # フォームデータが送信された場合
        form = MemoryForm(request.POST)
        if form.is_valid():
            # フォームデータを保存
            memory = form.save()
            # 保存後は詳細ページにリダイレクト
            return redirect('memolog:memory_detail', pk=memory.pk)
    else:
        # GETリクエストの場合は空のフォームを表示
        form = MemoryForm()
    
    return render(request, 'memolog/memory_form.html', {'form': form})
