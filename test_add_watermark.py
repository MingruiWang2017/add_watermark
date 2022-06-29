import argparse
import unittest
from unittest import mock
import os
import sys
from PIL import Image
import add_watermark


class TestWatermark(unittest.TestCase):
    def setUp(self) -> None:
        self.img = Image.new('RGB', (1280, 1080), color=(128, 0, 255))
        self.img_path = './images/temp.jpg'
        self.img.save(self.img_path)

    def tearDown(self) -> None:
        if os.path.exists('./images/temp.jpg'):
            os.remove('./images/temp.jpg')
        if os.path.exists('./out_images/out.jpg'):
            os.remove('./out_images/out.jpg')
        if os.path.exists('./out_images/out_with_watermark.jpg'):
            os.remove('./out_images/out_with_watermark.jpg')

    def test_read_origin_photo(self):
        image, h, w = add_watermark.read_origin_photo(self.img_path)
        self.assertEqual(h, 1280)
        self.assertEqual(w, 1080)

    def test_read_origin_photo_rotate(self):
        image, h, w = add_watermark.read_origin_photo(self.img_path, 90)
        self.assertEqual(h, 1080)
        self.assertEqual(w, 1280)

    def test_make_text_picture(self):
        text_pic = add_watermark.make_text_picture(
            1280, 1080, "test", r'./fonts/STSONG.TTF')
        self.assertTupleEqual(text_pic.size, (1280 * 2, 1080 * 2))

    def test_combine(self):
        origin_photo, h, w = add_watermark.read_origin_photo(self.img_path)
        text_pic = add_watermark.make_text_picture(
            1280, 1080, "test", r'./fonts/STSONG.TTF')
        add_watermark.combine(origin_photo, text_pic)
        self.assertTrue(os.path.exists('./out_images/out.jpg'))

    def test_get_args(self):
        sys.argv = ['add_watermark.py', '--photo_angle=90', '--new_image_name=out_with_watermark.jpg', 
                    '--text_color=#123456', '--text_size=80', '--text_angle=45', '--text_alpha=0.4',
                     './images/temp.jpg', 'test']
        args = add_watermark.get_args()
        self.assertEqual(args.photo_path, './images/temp.jpg')
        self.assertEqual(args.text, 'test')
        self.assertEqual(args.photo_angle, 90)
        self.assertEqual(args.new_image_name,
                         'out_with_watermark.jpg')
        self.assertEqual(args.font_path, './fonts/STSONG.TTF')
        self.assertEqual(args.text_angle, 45)
        self.assertEqual(args.text_color, '#123456')
        self.assertEqual(args.text_size, 80)
        self.assertEqual(args.text_alpha, 0.4)

    def test_main(self):
        add_watermark.get_args = mock.Mock(return_value=argparse.Namespace(photo_path='./images/temp.jpg',
                                                                           text='test',
                                                                           photo_angle=90,
                                                                           new_image_name='out_with_watermark.jpg',
                                                                           font_path='./fonts/STSONG.TTF',
                                                                           text_angle=45,
                                                                           text_color='#123456',
                                                                           text_size=80,
                                                                           text_alpha=0.4))
        add_watermark.main()
        self.assertTrue(os.path.exists('./out_images/out_with_watermark.jpg'))


if __name__ == '__main__':
    unittest.main()
