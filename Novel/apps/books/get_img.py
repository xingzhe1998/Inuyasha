import requests
import re
r = requests.get('https://image.so.com/i?src=360pic_strong&z=1&i=0&cmg=7abc82423e2d5c68079991aa6681297b&q=%E7%8E%84%E5%B9%BB%E5%9B%BE%E7%89%87#/')
a = r.text
print(a)
li =  re.findall(r"https://p1.ssl.qhimgs1.com/static/.+[.]jpg",a)

print(li)
# <a data-v-1aa2f1c5="" id="" href="/view?src=360pic_strong&amp;z=1&amp;i=0&amp;cmg=7abc82423e2d5c68079991aa6681297b&amp;q=%E7%8E%84%E5%B9%BB%E5%9B%BE%E7%89%87&amp;correct=%E7%8E%84%E5%B9%BB%E5%9B%BE%E7%89%87&amp;ancestor=list&amp;cmsid=fac698b41eab0305599581f490521cf7&amp;cmran=0&amp;cmras=1&amp;cn=0&amp;gn=0&amp;kn=50&amp;fsn=130&amp;adstar=0&amp;clw=235#id=d174e1698e625f9bbb597614df0a7c55&amp;currsn=0&amp;ps=102&amp;pc=102" target="_blank"><span data-v-1aa2f1c5="" class="img" style="height: 138px;"><img data-v-1aa2f1c5="" src="https://p1.ssl.qhimgs1.com/sdr/400__/t014b42a80405bf2e6d.jpg" alt="玄幻背景图片_玄幻背景素材下载_我图网" style="height: 138px; width: 235px; left: 0px; top: 0px;"><i data-v-1aa2f1c5="" class="mask"></i><!----></span><span data-v-1aa2f1c5="" title="玄幻背景图片_玄幻背景素材下载_我图网" class="txt">玄幻背景图片_玄幻背景素材下载_我图网</span></a>
