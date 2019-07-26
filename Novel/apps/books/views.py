from django.db.models import Count
from django.shortcuts import render
from apps.books.models  import Heat, Novel, Flash,Generalize
from django.db.models import  Q
import re
from django.http import FileResponse
import json
from apps.books.china_num import to_chinese4
import random
import os

# Create your views here.
kinds ={'xh':'玄幻奇幻',"ds":'都市言情','kh':'科幻灵异',"dm":'耽美同人','np':'女频言情','ls':'历史军事','wx':'武侠仙侠','wy':'网游竞技'}

def index(request):
    tops = {}
    left = {}
    unfind = ""
    all = Novel.objects.all()
    new_novel = {"one":all[0],"two":all[1]}
    if request.method == "POST":
        novel =all.filter(novel_name=request.POST.get('w'))
        if len(novel) == 0:
            unfind = "没有你要找的小说"
        else:
            return mulu(request, novel[0].id)
    for  key ,kind_name in kinds.items():
        novels = all.filter(kind = kind_name).order_by("-heat__read_num")
        if len(novels) > 2:
            left[key] = novels[0:2]
        else:
            left[key] = novels
    flash1 = Flash.objects.get(pk=2)
    flash2 = Flash.objects.get(pk=3)
    flash3 = Flash.objects.get(pk=4)
    man_novel = all.exclude(Q(kind="女频言情") and Q(kind = "耽美同人"))
    if len(man_novel)>6:
        man_novel = man_novel[0:6]
    woman_novel = all.filter(Q(kind="女频言情") | Q(kind = "耽美同人"))
    if len(woman_novel)>6:
        woman_novel = woman_novel[0:6]
    old = all
    click_order = old.order_by("-heat__read_num")
    if len(click_order) > 6:
        click_order = list(click_order[0:6])
    down_order = old.order_by("-heat__down_load")
    if len(down_order) > 6:
        down_order = list(down_order[0:6])
    nv = all.values("novel_name")
    collect = nv.annotate(Count("bookshelf")).order_by("-bookshelf__count")[:6]
    all_generalize = Generalize.objects.all()
    for key ,value in kinds.items():
        top = all.filter(kind=value).order_by("-heat__read_num")[0]
        tops[value] = top
    return render(request, "index.html",{"unfind":unfind,
                                         "left":left,
                                         "flash1":flash1,"flash2":flash2,"flash3":flash3,
                                         "new_novel":new_novel,
                                         "man_novel":man_novel,
                                         "woman_novel":woman_novel,
                                         "click_order":click_order,
                                         "down_order":down_order,
                                         "collect":collect,
                                         "all_generalize":all_generalize,
                                         "tops":tops,
                                         }
                  )


def article(request,id):
    flash = Flash.objects.get(pk=id)
    flash_text = None
    with open(flash.text, 'r', encoding="utf-8") as fp:
        flash_text = fp.readlines()
    return render(request,"flash.html",{"flash":flash,"flash_text":flash_text})



def kind(request,kind_name,num=0):
    chapter_list = []
    user = request.user
    kind_inf = None
    with open("static/setting.txt",'r',encoding="utf-8")as fp:
        kind_inf = json.loads(fp.read())
    if num < 0:
        num = 0
    novel_set = Novel.objects.filter(kind=kind_name)
    lenght = len(novel_set)
    n =lenght
    if num >= lenght:
        num = num-10
    pg_len = 1
    while True:
        n = n - 10
        if n > 0 :
            pg_len += 1
        else:
            break
    # print(lenght)
    if  num+10 > lenght:
        novel_set = novel_set[num:(num+(lenght-num))]
    else:
        novel_set = novel_set[num:(num+10)]
    if num -10 < 0:
        last_num = num
    else:
        last_num = num - 10
    next_num = num + 10
    old = Novel.objects.filter(kind=kind_name)
    click_order = old.order_by("-heat__read_num")
    if len(click_order) > 10:
        click_order = list(click_order[0:10])
    down_order = old.order_by("-heat__down_load")
    if len(down_order) > 10:
        down_order = list(down_order[0:10])
    novel_all = Novel.objects.all()
    i = random.randint(0,len(novel_all)-10)
    other = novel_all[i:(i+10)]
    collect_id = request.GET.get('collect_id', '')
    print(collect_id)
    novels_numb  = Novel.objects.all().count()
    # 判断用户是否已经登录
    info = {
        'code': 200,
        'msg': '收藏成功!',
    }
    if collect_id:
        # 判断用户是否已经登录
        if not user.is_authenticated:
            info = {
                'code':300,
                'msg':'没有登录就无法收藏小说哦',
            }
        else:
            # 判断用户是否已经收藏过小说
            novel = user.shelf.books.filter(id=collect_id)
            print(novel)
            if novel:
                info = {
                    'code':301,
                    'msg':'您已经收藏过本小说啦',
                }
            else:
                # 将书本实例保存到用户书架里
                new_novel = Novel.objects.get(id=collect_id)
                # many2many字段信息保存
                user.shelf.books.add(new_novel)
                user.shelf.save()
                # 用户没有阅读，直接收藏，默认从第一章开始读书
                if not user.shelf.chapters:
                    collect_info = {}
                    collect_info[new_novel.id] = 1
                    user.shelf.chapters = json.dumps(collect_info)
                    user.shelf.save()
        print(user.shelf.chapters)
    else:info={}

    return render(request,"list.html",{"novel_set":novel_set,
                                       "pg_num":int(num/10)+1,
                                       "pg_len":pg_len,'kind_name':kind_name,
                                       "next":next_num,"last":last_num,
                                       "kind_text":kind_inf[kind_name][0],
                                       "kind_img":kind_inf[kind_name][1],
                                       "click_order":click_order,
                                       "down_order":down_order,
                                       "other":other,
                                       "info":info,
                                       "novels_numb":novels_numb,
                                       }
                  )




def mulu(request,id=1):
    li= []
    novel = Novel.objects.get(pk=id)
    name = novel.novel_name
    section = json.loads(novel.section_num)
    print(section)
    se_num = {}
    # download/万古天帝.txt
    # django工作目录为项目目录下第一层，与apps平级
    with open(novel.file, 'r', encoding="utf-8") as fp:
        for key, value in section.items():
            se = to_chinese4(int(key))
            for  line in fp:
                if re.search(f"{value}.*[\n]", line) or re.search(f"第{key}章.*[\n]", line) or re.search(f"第{se}章.*[\n]", line) :
                    se_num[key] = line
                    break
            else:
                break
    li = []
    for key ,value in se_num.items():
        li.append((key,value))
    # print(li)
    return render(request,"mulu.html",{"li":li,"novel_id":id,"se_num":len(se_num),"name":name})


def look_novel(request,id=1,sec_num = 1):
    novel = Novel.objects.get(pk=id)
    print(novel.heat)
    if sec_num == 1:
        novel.heat.read_num = novel.heat.read_num + 1
        novel.save()
    data = []
    section = json.loads(novel.section_num)
    se_re = section[str(sec_num)]
    print(se_re)
    with open(novel.file,'r',encoding='utf-8') as fp:
        pos = fp.seek(0, 2)
        fp.seek(0)
        flag = 2
        while flag:
            text = fp.readline()
            if flag == 1 and re.search(r'第.*章', text) is None and fp.tell() != pos:
                data.append(text)
            elif flag == 2:
                pass
            else:
                flag -= 1
            if re.search(se_re, text) is not None and flag == 2:
                data.append(text)
                print(data)
                flag -= 1
        self_url = f"/list/novel{id}/section/section:{sec_num}/"
        user = request.user
        if user.is_authenticated:             # 将登录用户的阅读信息暂存在当前session中
            if not user.shelf.chapters:       # 用户第一次阅读记录，此时数据库中还没有数据
                js = {}
                js[novel.id] = sec_num
                user.shelf.chapters = json.dumps(js)
                user.shelf.save()
            else:
                js = json.loads(user.shelf.chapters)    # 将每一条阅读记录去重之后保存到数据库
                # 最多保存二十条数据
                if len(js)>20:
                    for i in range(1,20):
                        js.popitem()
                js[str(novel.id)] = sec_num    # 字典自动去重的特性，阅读同一本书时，只能储存一个键值对
                user.shelf.chapters = json.dumps(js)
                user.shelf.save()
            print(user.shelf.chapters)

        if  section.get(str(sec_num+1)) is None:
            next_url = self_url
        else:
            next_url = f"/list/novel{id}/section/section:{sec_num+1}/"
        if  section.get(str(sec_num-1)) is None:
            last_url = self_url
        else:
            last_url = f"/list/novel{id}/section/section:{sec_num-1}/"
        return render(request, "novel.html", {"data": data,"pg_len":len(section),"pg_num":sec_num,"last":last_url,"next":next_url,"novel_id":id})

def down_load(request,id=0):
    novel = Novel.objects.get(pk=id)
    novel.heat.down_load = novel.heat.down_load +1
    file=open(novel.file,'rb')
    response =FileResponse(file)
    response['Content-Type']='APPLICATION/OCTET-STREAM'
    response['Content-Disposition'] =f'attachment;filename={id}.txt'
    response['Content-Length'] = os.path.getsize(novel.file)  # 传输给客户端的文件大小
    novel.save()
    return response

# def add_hot(request):
#     i = 1
#     novels = Novel.objects.all()
#     for novel in novels:
#         print(i)
#         click_num = random.randint(500, 2000)
#         download_num = random.randint(1, 200)
#         new_heat = Heat(read_num=click_num,down_load=download_num)
#         new_heat.save()
#         novel.heat = new_heat
#         novel.save()
#         i=i+1
#     return  HttpResponse(request,"<p>aaaa</p>")
