import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance


def read_origin_photo(photo_path, photo_angle=0):
    """
    获取图像内容与尺寸

    photo_path：图片路径
    photo_angle: 图片旋转角度
    """
    origin_photo = Image.open(photo_path)
    origin_photo = origin_photo.convert('RGBA')
    origin_photo = origin_photo.rotate(photo_angle, expand=True)
    h, w = origin_photo.size
    return origin_photo, h, w

# def get_color(text_color):
#     r = int(text_color[1:3], base=16)
#     g = int(text_color[3:5], base=16)
#     b = int(text_color[5:7], base=16)
#     return r, g, b


def make_text_picture(h, w, text, font_path, font_size=40, angle=-45, color=(0, 0, 0)):
    """
    制作水印图片

    h: 原图高度
    w: 原图宽度
    font_path：字体文件路径
    font_size：字体大小
    angle：字体旋转角度
    color：字体颜色
    """
    text_pic = Image.new('RGBA', (4 * h, 4 * w), (255, 255, 255, 255))
    fnt = ImageFont.truetype(font_path, size=font_size)

    text_d = ImageDraw.Draw(text_pic)

    # a, b 分别控制水印的列间距和行间距，默认为字体的2倍列距，4倍行距
    a, b = 2, 4
    for x in range(10, text_pic.size[0] - 10, a * font_size * len(text)):
        for y in range(10, text_pic.size[1] - 10, b * font_size):
            text_d.multiline_text((x, y), text, fill=color, font=fnt)

    # 旋转水印
    text_pic = text_pic.rotate(angle)
    # 截取水印部分图片
    text_pic = text_pic.crop((h, w, 3 * h, 3 * w))
    # text_pic.show()
    return text_pic


def combine(origin_photo, text_pic, alpha=0.2, out_name='out.jpg'):
    """
    为图片添加水印并保存
    origin_photo: 原图内容
    text_pic: 要添加的水印图片
    alpha：水印的不透明度
    out_name: 输出图片的文件名
    """
    # 合并水印图片和原图
    text_pic = text_pic.resize(origin_photo.size)
    out = Image.blend(origin_photo, text_pic, alpha)
    out = out.convert('RGB')
    # 增强图片对比度
    enhance = ImageEnhance.Contrast(out)
    out = enhance.enhance(1.0 / (1 - alpha))
    out_path = os.path.join('./out_images/', out_name)
    out.save(out_path)
    # out.show()


def get_args(args=sys.argv[1:]):
    """解析命令行参数"""
    print(args)
    parser = argparse.ArgumentParser(args)
    parser.add_argument('photo_path', help='图片路径，如：1.jpg或./images/1.jpg')
    parser.add_argument('text', help="要添加的水印内容")
    parser.add_argument('--photo_angle', dest='photo_angle', type=int, default=0,
                        help='原图片旋转角度，默认为0，不进行旋转')
    parser.add_argument('--new_image_name', dest='new_image_name', default=None,
                        help='输出图片的名称， 默认为"原图片名_with_watermark.jpg", 图片保存在out_images目录下')
    parser.add_argument('--font_path', dest='font_path', default=r"./fonts/STSONG.TTF",
                        help='要使用的字体路径，如 STSONG.TTF，windows可在C:\Windows\Fonts查找字体')
    parser.add_argument('--text_angle', dest='text_angle', type=int, default=-45,
                        help='水印的旋转角度，0为水平，-90位从上向下垂直, 90为从下向上垂直，默认-45')
    parser.add_argument('--text_color', dest='text_color', default='#000000',
                        help="水印颜色，默认#000000（黑色）")
    parser.add_argument('--text_size', dest='text_size', type=int,
                        default=40, help='水印字体的大小， 默认40')
    parser.add_argument('--text_alpha', dest='text_alpha', type=float,
                        default=0.2, help='水印的不透明度，建议0.2~0.3，默认0.2')
    return parser.parse_args()


def main():
    """执行添加水印操作"""
    args = get_args()

    photo_path = args.photo_path
    text = args.text
    if not photo_path or not text:
        print('必须指定图片路径和水印文字')
        sys.exit(-1)

    photo_angle = args.photo_angle
    font_path = args.font_path
    text_size = args.text_size
    text_angle = args.text_angle

    origin_photo, h, w = read_origin_photo(photo_path, photo_angle)
    text_pic = make_text_picture(h, w, text, font_path,
                                 font_size=text_size, angle=text_angle,
                                 color=args.text_color)

    new_image_name = args.new_image_name
    photo_name = os.path.split(photo_path)[-1].split('.')[0]  # 获取图片名称
    if new_image_name is None:
        new_image_name = photo_name + '_with_watermark.jpg'
    text_alpha = args.text_alpha

    combine(origin_photo, text_pic, alpha=text_alpha,
            out_name=new_image_name)


if __name__ == '__main__':
    main()
