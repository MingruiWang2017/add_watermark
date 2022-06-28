import unittest
import os
from PIL import Image
import add_watermark

class TestWatermark(unittest.TestCase):
    def setUp(self) -> None:
        self.img = Image.new('RGB', (1280, 1080), color=(128, 0, 255))
        self.img_path= './images/temp.jpg'
        self.img.save(self.img_path)

    def tearDown(self) -> None:
        if os.path.exists('./images/temp.jpg'):
            os.remove('./images/temp.jpg')
        if os.path.exists('./out_images/out.jpg'):
            os.remove('./out_images/out.jpg')

    def test_read_origin_photo(self):
        image, h, w = add_watermark.read_origin_photo(self.img_path)
        self.assertEqual(h, 1280)
        self.assertEqual(w, 1080)

    def test_read_origin_photo_rotate(self):
        image, h, w = add_watermark.read_origin_photo(self.img_path, 90)
        self.assertEqual(h, 1080)
        self.assertEqual(w, 1280)
    
    def test_make_text_picture(self):
        text_pic = add_watermark.make_text_picture(1280, 1080, "test", r'./fonts/STSONG.TTF')
        self.assertTupleEqual(text_pic.size, (1280 * 2, 1080 * 2))

    def test_combine(self):
        origin_photo, h, w = add_watermark.read_origin_photo(self.img_path)
        text_pic = add_watermark.make_text_picture(
            1280, 1080, "test", r'./fonts/STSONG.TTF')
        add_watermark.combine(origin_photo, text_pic)
        self.assertTrue(os.path.exists('./out_images/out.jpg'))




if __name__ == '__main__':
    unittest.main()