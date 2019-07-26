from PIL import Image

# 先获取到图片文件
# path = '/Users/apple/PycharmProjects/Novel/media/15/avator/20190718/1563414002.513477.jpg'
def make_thumb(path, size):
    pixbuf = Image.open(path)
    # 查看原图片规格信息
    width, height = pixbuf.size
    if width>size:
        # 缩小比例
        delta = width/size
        height = int(height/delta)
        # thumbnail => 生成指定格式的缩略图
        pixbuf.thumbnail((size, height), Image.ANTIALIAS)
        return pixbuf