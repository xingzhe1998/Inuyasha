from django.shortcuts import render
from apps.books.models import Novel
import json
# Create your views here.

def shelf(request):
    user = request.user
    # 书架实例
    ushelf = user.shelf
    # 阅读历史
    read_history = ushelf.chapters
    print(read_history)
    collect_id = request.GET.get('collect_id', '')
    if collect_id:
        ushelf.books.remove(Novel.objects.get(id=collect_id))
        chap = json.loads(read_history)
        chap.pop(str(collect_id))
        ushelf.save()
    # 已经收藏的书本
    novels = ushelf.books.all()
    if read_history:
        for novel in novels:
            chapter = json.loads(read_history).get(str(novel.id), 1)
            novel.current_chapter = chapter
            finsh = int(chapter)/int(len(json.loads(novel.section_num)))
            finsh_dem = '%.3f'%(finsh)
            ff = float(finsh_dem)*100
            read_p = '%.1f'%ff
            novel.read_progress = read_p

    # else:
    #     for novel in novels:
    #         novel.current_chapter = 1
    #         print('xxx', novel.current_chapter)
    return render(request, 'shelf.html', {'novels':novels})


def drop_novel(request):
    pass