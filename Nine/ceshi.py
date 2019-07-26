# import requests

from urllib.parse import quote
import string
import requests
from urllib.request import urlopen
import urllib.request
import http.cookiejar
import ssl

url = 'http://xiazai.xqishu.com/txt/君临战国.txt'
new_url = 'http://xiazai.xqishu.com/txt/%E9%AC%BC%E7%81%B5%E7%B2%BE%E6%80%AA%E4%B9%9F%E8%AE%A4%E6%A0%BD.txt'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'cookies': '__music_index__=2; ASPSESSIONIDQCCDCART=ADCJOKECHKHHPNKBMIIHEKAH; NewAspUsers%5FOnline=UserSessionID=11331555654; UM_distinctid=16bbcaa112913e-0cb611d1b8ed31-7a1437-1fa400-16bbcaa112a68; 37cs_user=37cs52163986298; 37cs_show=69; __music_index__=2; CNZZDATA1642736=cnzz_eid%3D1136135112-1562239206-null%26ntime%3D1562239206; bdshare_firstime=1562240402471; _d_id=3533d113318a3ac920446bc8666b3b; CNZZDATA1835761=cnzz_eid%3D195897192-1562236194-null%26ntime%3D1562247708; Hm_lvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562238391,1562238967,1562247135,1562248118; 37cs_pidx=4; 37cs_pennding16859=true; CS_pending16859=true; Hm_lpvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562248144',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

request = urllib.request.Request(new_url, headers=headers)

# with urlopen(request) as file:
#     for line in file:
#             content = file.readline().decode('gbk')
#             with open('e.txt','a', encoding='utf-8') as f:
#                 f.write(content)

# ConnectionError
# with urlopen(request) as file:
#     print(type(file.headers['Content-Length']))
# 'http://xiazai.xqishu.com/txt/%E5%90%9B%E4%B8%B4%E6%88%98%E5%9B%BD.txt'
# 'http://xiazai.xqishu.com/txt/%E5%90%9B%E4%B8%B4%E6%88%98%E5%9B%BD.txt'

print(r'C:\Users\Administrator\Desktop\Qshu')
# with urlopen(new_url) as file:
#     for line in file:
#         content = file.readline().decode('gbk')
#         with open(r'C:\Users\Administrator\Desktop\Qshu\{}.txt'.format(item['book_title']), 'a', encoding='utf-8') as f:
#             f.write(content)

#
