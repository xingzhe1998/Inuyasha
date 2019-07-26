from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

import json
import re
import random
from apps.books.models import Heat,Flash,Novel
# Create your views here.

def base(request):
    # novel = Novel.objects.get(pk=1)
    # with open(r'download/万古天帝.txt', 'r', encoding='utf-8') as f:
    #     print(f.read())
    # section = {}
    # with open("/Users/apple/PycharmProjects/Novel/download/斗破苍穹.txt", 'r', encoding='utf-8') as fp:
    #     novel = fp.read()
    #     li = list(re.findall(r"(第.*章).*\n", novel))
    #     i = 1
    #     for se in li:
    #         section[i] = se
    #         i = i + 1
    # section = json.dumps(section)
    # heat = Heat(down_load=500, read_num=500)
    # heat.save()
    # novel = Novel(novel_name="斗破苍穹",
    #               kind="玄幻奇幻",
    #               author_name="天蚕土豆",
    #               brief_introduction="这里是属于斗气的世界，没有花俏艳丽的魔法，有的，仅仅是繁衍到巅峰的斗气！",
    #               picture="/static/image/玄幻/dpcq.jpg",
    #               file=r"/Users/apple/PycharmProjects/Novel/download/斗破苍穹.txt",
    #               heat=heat,
    #               section_num=section
    #               )
    # novel.save()


    # novels = Novel.objects.filter(kind="耽美同人")
    # i = 1
    # for novel in novels:
    #     novel.picture = rf"/static/image/耽美/dm{i}.jpg"
    #     novel.save()
    #     i = i + 1
    # novels = Novel.objects.all()
    # for novel in novels:
    #     heat = Heat()
    #     heat.read_num = 400 + random.randint(1,600)
    #     heat.down_load = 300 + random.randint(1,200)
    #     heat.save()
    #     novel.heat = heat
    #     novel.save()
    return redirect('/index/')
    # section1 = {}
    # with open(r"/Users/apple/PycharmProjects/Novel/download/我欲封天.txt", 'r', encoding='utf-8') as fp:
    #     novel = fp.read()
    #     li = list(re.findall(r"(第.*章).*\n", novel))
    #     i = 1
    #     for se in li:
    #         section1[i] = se
    #         i = i + 1
    # section1 = json.dumps(section)
    # heat1 = Heat(down_load=500, read_num=500)
    # heat1.save()
    # novel = Novel(novel_name="我欲封天",
    #               kind="玄幻奇幻",
    #               author_name="耳根", # brief_introduction
    #               brief_introduction="个“我命如妖欲封天”的世界！这是耳根继《仙逆》《求魔》后，创作的第三部长篇小说《我欲封天》",
    #               picture="/static/image/玄幻/wy.jpg",
    #               file=r"/Users/apple/PycharmProjects/Novel/download/我欲封天.txt",
    #               heat=heat1,
    #               section_num=section1
    #               )
    # novel.save()