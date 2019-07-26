import json
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def sendsms(mobile, captcha):
    flag = True
    url = 'https://open.ucpaas.com/ol/sms/sendsms'
    # 准备一下头,声明body的格式
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {
        'appid':'32eec568bf184618a222bebbefb4bd5b',
        'sid':'424ba67011f7dac65fb5b6a09241c6a1',
        'token':'ebe77f586cf5cef1e22baeff26311ea9',
        'templateid':'461339',
        "param": str(captcha),
        "mobile":mobile,
    }
    try:
        # 将字典格式化成bytes格式
        data = json.dumps(params).encode('utf-8')
        # 创建一个request,放入我们的地址、数据、头
        request = urllib.request.Request(url, data, headers)
        html = urllib.request.urlopen(request).read().decode('utf-8')
        print(html)
        '''
        {"code":"100005","count":"0","create_date":"","mobile":"13787084379","msg":"发送请求的IP不在白名单内","smsid":"","uid":""}
        '''
        code = json.loads(html)["code"]
        print(f"code:{code}")
        if code == "000000":
            flag = True
        else:
            flag = False
    except Exception as ex:
        print(ex)
        flag = False
    return flag

# ip白名单添加的自己手机热点ip有效???
if __name__ == "__main__":
    sendsms('13787084379', '123456')