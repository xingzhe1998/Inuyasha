# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request
from requests.exceptions import ConnectionError
from scrapy import Request
from scrapy.exceptions import DropItem
from Nine import settings
import pymysql
import re
import json
import os
import time
# raise DropItem丢弃当前item
class TextPipeline(object):
    def __init__(self):
        self.max_length = 60
        self.base_path = '/User/apple/PycharmProjects/Novel/download'
        self.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'cookies': '__music_index__=2; ASPSESSIONIDQCCDCART=ADCJOKECHKHHPNKBMIIHEKAH; NewAspUsers%5FOnline=UserSessionID=11331555654; UM_distinctid=16bbcaa112913e-0cb611d1b8ed31-7a1437-1fa400-16bbcaa112a68; 37cs_user=37cs52163986298; 37cs_show=69; __music_index__=2; CNZZDATA1642736=cnzz_eid%3D1136135112-1562239206-null%26ntime%3D1562239206; bdshare_firstime=1562240402471; _d_id=3533d113318a3ac920446bc8666b3b; CNZZDATA1835761=cnzz_eid%3D195897192-1562236194-null%26ntime%3D1562247708; Hm_lvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562238391,1562238967,1562247135,1562248118; Hm_lpvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562251398',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }

    def process_item(self, item, spider):
        try:
            print('正在下载小说{}...'.format(item['book_title']))
            request = urllib.request.Request(url=item['download_url'], headers=self.headers)
            item['file_path'] = self.base_path + '\{}.txt'.format(item['book_title'])
            with urllib.request.urlopen(request) as file:
                if file.headers['Content-Length'] == '391':
                    raise DropItem('错误网页...damn')
                else:
                    for line in file.readlines():
                        with open(item['file_path'], 'a', encoding='utf-8') as fp:
                            fp.write(line.decode('gbk', 'ignore'))

            if len(item['book_intro']) > self.max_length:
                item['book_intro'] = item['book_intro'][:self.max_length].strip() + '...'

        except ConnectionError:
            print('get connectionerror...damn')
            return Request(item['download_url'], callback=self.process_item, dont_filter=True)

        section = {}
        with open(f"/User/apple/PycharmProjects/Novel/download/{item['book_title']}.txt", 'r', encoding='utf-8') as fp:
            novel = fp.read()
            li = list(re.findall(r"(第.*章).*\n", novel))
            i = 1
            for se in li:
                section[i] = se
                i = i + 1
        if section == {}:
            item['section'] =  None
        else:
            item['section'] = json.dumps(section)
        return item


class MysqlPipline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)

        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        # try:
        print('正在插入数据........')
        # 查重处理
        self.cursor.execute(
            """select * from app1_novel where novel_name=%s;""",
            item['book_title'])
        # 是否有重复数据
        repetition = self.cursor.fetchone()

        # 重复
        if repetition or item['section'] is  None:
            pass

        else:

            # 插入数据
            print('到这了')
            self.cursor.execute(
                """INSERT INTO app1_novel(kind, novel_name, author_name, file,brief_introduction,section_num) VALUES(%s,%s,%s,%s,%s,%s);""",
                (
                    item['book_type'],
                    item['book_title'],
                    item['author'],
                    item['file_path'],
                    item['book_intro'],
                    item['section'],
                ))

        # 提交sql语句
        self.connect.commit()

        # except Exception as error:
        #     出现错误时打印错误日志
        #     print('get excption...')
        return item
