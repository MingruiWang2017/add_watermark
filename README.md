# add_watermark

为图片添加全屏水印

---

## 安装依赖

工具使用需要安装 pillow,直接安装：`pip install pillow`

或者 `pip install -r requirements.txt` 

---
## 使用方法

### 查看帮助信息
```
$ python add_watermark.py -h
usage: add_watermark.py [-h] [--photo_angle PHOTO_ANGLE] [--new_image_name NEW_IMAGE_NAME] [--font_path FONT_PATH]
                        [--text_angle TEXT_ANGLE] [--text_color TEXT_COLOR] [--text_size TEXT_SIZE] [--text_alpha TEXT_ALPHA]
                        photo_path text

positional arguments:
  photo_path            图片路径，如：1.jpg或./images/1.jpg
  text                  要添加的水印内容

options:
  -h, --help            show this help message and exit
  --photo_angle PHOTO_ANGLE
                        原图片旋转角度，默认为0，不进行旋转
  --new_image_name NEW_IMAGE_NAME
                        输出图片的名称， 默认为"原图片名_with_watermark.jpg", 图片保存在out_images目录下
  --font_path FONT_PATH
                        要使用的字体路径，如 STSONG.TTF，windows可在C:\Windows\Fonts查找字体
  --text_angle TEXT_ANGLE
                        水印的旋转角度，0为水平，-90位从上向下垂直, 90为从下向上垂直，默认-45
  --text_color TEXT_COLOR
                        水印颜色，默认#000000（黑色）
  --text_size TEXT_SIZE
                        水印字体的大小， 默认40
  --text_alpha TEXT_ALPHA
                        水印的不透明度，建议0.2~0.3，默认0.2
```

### 添加默认水印

```
$ python add_watermark.py ./images/1.jpg "房东的猫"
```
原图：

![原图](./images/1.jpg)

添加默认格式水印：

![添加默认水印](./out_images/1_with_watermark.jpg)


### 添加蓝色其他字体水印
```
$ python add_watermark.py --new_image_name="2.jpg" --text_color="#0000FF" --font_path="./fonts/简卡通.TTF" --text_alpha=0.1 ./images/1.jpg "寄 没有地址的信"
```

添加蓝色水印：

![添加蓝色水印](./out_images/2.jpg)

### 旋转原图片
```
$ python add_watermark.py --photo_angle=90 --new_image_name="3.jpg" --text_alpha=0.3 --text_color="#22FF22" --font_path="./fonts/简卡通.TTF" ./images/2.jpg "我可以 陪你去看星星"
```

旋转后的水印图片：

![旋转后的水印图片](./out_images/2_with_watermark.jpg)