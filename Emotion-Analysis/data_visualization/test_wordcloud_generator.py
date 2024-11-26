import unittest

import imageio
from wordcloud import ImageColorGenerator

from wordcloud_generator import (
    load_text_data,
    generate_wordcloud,
    save_wordcloud,
    beautify_images,
    save_top_words,
    wordcloud_generator,
    wordclouds_generator
)
import os
from PIL import Image

FONT_PATH = ('E:\\github_repositories\\Emotion-Analysis-Project'
             '\\Emotion-Analysis\\data_visualization'
             '\\fonts\\NotoSansSC-Regular.ttf')
IMAGE_PATH = ('E:\\github_repositories\\Emotion-Analysis-Project'
              '\\Emotion-Analysis\\data_visualization'
              '\\test_utils\\test_background.png')


class TestWordCloudGenerator(unittest.TestCase):

    def test_load_text_data(self):
        # 测试项：确保函数能正确读取CSV文件并返回所有行的第一列数据。
        test_file_path = ('E:\\github_repositories\\Emotion-Analysis-Project'
                          '\\Emotion-Analysis\\data_visualization'
                          '\\test_utils\\test_data.csv')  # 假设有一个测试用的CSV文件
        expected_text = "这是一个测试"  # 假设CSV文件第一列的内容
        with open(test_file_path, 'w', encoding='utf-8-sig') as f:
            f.write(expected_text + '\n')
        self.assertEqual(load_text_data(test_file_path), expected_text)
        os.remove(test_file_path)  # 测试后删除测试文件

    def test_generate_wordcloud(self):
        # 测试项：确保函数能根据给定参数生成词云。
        text = "你好 世界"
        font_path = FONT_PATH
        bg_image = imageio.imread(IMAGE_PATH)
        image_color = ImageColorGenerator(bg_image)
        wc = generate_wordcloud(text, font_path, bg_image, image_color)
        self.assertIsNotNone(wc)

    def test_save_wordcloud(self):
        # 测试项：确保函数能将词云保存为图像文件。
        text = "你好 世界"
        font_path = FONT_PATH
        bg_image = imageio.imread(IMAGE_PATH)
        image_color = ImageColorGenerator(bg_image)
        wc = generate_wordcloud(text, font_path, bg_image, image_color)
        filename = 'test_wc'
        save_path = ''
        save_wordcloud(wc, filename, dpi=150, save_path=save_path)
        self.assertTrue(os.path.exists(f'{save_path}{filename}.png'))
        os.remove(f'{save_path}{filename}.png')

    def test_beautify_images(self):
        # 测试项：确保函数能美化图像。
        filename = 'test_beautify'
        save_path = ''
        # 创建一个测试图像
        img = Image.new('RGB', (100, 100), color='red')
        img.save(f'{save_path}{filename}.png')
        beautify_images(filename, save_path)
        # 测试美化后的图像是否存在
        self.assertTrue(os.path.exists(f'{save_path}{filename}.png'))
        os.remove(f'{save_path}{filename}.png')

    def test_save_top_words(self):
        # 测试项：确保函数能保存词云中的高频词汇。
        wc = generate_wordcloud("Hello world", FONT_PATH, None, None)
        filename = 'test_top_words'
        save_path = ''
        save_top_words(wc, filename, save_path)
        self.assertTrue(os.path.exists(f'{save_path}{filename}.txt'))
        os.remove(f'{save_path}{filename}.txt')

    def test_wordcloud_generator(self):
        # 测试项：确保函数能生成特定情感的词云并保存。
        data_files = {
            'test': {
                'text': 'E:\\github_repositories\\Emotion-Analysis-Project'
                        '\\Emotion-Analysis\\data_visualization'
                        '\\test_utils\\test_data.csv',
                'background': IMAGE_PATH
            }
        }
        save_path = ('E:\\github_repositories\\Emotion-Analysis-Project'
                     '\\Emotion-Analysis\\data_visualization\\test_utils\\')
        font_path = FONT_PATH
        save_path_2 = ''
        wordcloud_generator('test', data_files['test'], save_path,
                            font_path, save_path_2)
        # 检查生成的词云文件是否存在
        self.assertTrue(os.path.exists('E:\\github_repositories'
                                       '\\Emotion-Analysis-Project'
                                       '\\Emotion-Analysis\\data_visualization'
                                       '\\test_utils\\wordcloud_test.png'))

    def test_wordclouds_generator(self):
        # 测试项：确保函数能生成所有情感的词云。
        wordclouds_generator()
        # 检查是否生成了所有词云文件
        self.assertTrue(os.path.exists('E:/github_repositories'
                                       '/Emotion-Analysis-Project'
                                       '/Emotion-Analysis/static'
                                       '/wordclouds/wordcloud_all.png'))
        self.assertTrue(os.path.exists('E:/github_repositories'
                                       '/Emotion-Analysis-Project'
                                       '/Emotion-Analysis/static'
                                       '/wordclouds/wordcloud_positive.png'))
        self.assertTrue(os.path.exists('E:/github_repositories'
                                       '/Emotion-Analysis-Project'
                                       '/Emotion-Analysis/static'
                                       '/wordclouds/wordcloud_negative.png'))


if __name__ == '__main__':
    unittest.main()
