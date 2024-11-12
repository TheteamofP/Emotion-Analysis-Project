import unittest
# unittest.mock用于编写和运行测试用例
from unittest.mock import patch, mock_open
import os
from utils.wordcloud_generator import (load_text_data, load_stopwords, generate_wordcloud, save_wordcloud,
                                       beautify_images, wordcloud_generator)
                                    # , cut_words


class TestWordCloudModule(unittest.TestCase):

    # 设置测试环境
    def setUp(self):
        # 设置测试数据文件和停用词文件的路径
        self.test_data_path = './tests_data/test_data.txt'
        self.test_stopwords_path = './tests_data/test_stopwords.txt'
        # 创建测试数据文件和停用词文件
        with open(self.test_data_path, 'w', encoding='utf-8-sig') as f:
            f.write('This is a test text for wordcloud.')
        with open(self.test_stopwords_path, 'w', encoding='utf-8-sig') as f:
            f.write('test\ntext')

    # 清理测试环境
    def tearDown(self):
        # 删除测试数据文件和停用词文件
        os.remove(self.test_data_path)
        os.remove(self.test_stopwords_path)

    # 测试load_text_data函数是否正确读取文件内容
    def test_load_text_data(self):
        # 模拟文件打开操作
        with patch('builtins.open', mock_open(read_data='Test text data')):
            result = load_text_data('./tests_data/test_data.txt')
            self.assertEqual(result, 'Test text data')

    # 测试load_text_data函数在文件不存在时的行为
    def test_load_text_data_file_not_found(self):
        # 模拟文件打开时抛出FileNotFoundError异常
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = load_text_data('./tests_data/non_existent_file.txt')
            self.assertIsNone(result)

    # # 测试cut_words函数
    # def test_cut_words(self):
    #     text = '这是一个测试文本'
    #     result = cut_words(text)
    #     self.assertEqual(result, '这是一个 测试 文本')

    # 测试load_stopwords函数是否正确读取停用词列表
    def test_load_stopwords(self):
        with patch('builtins.open', mock_open(read_data='stopword1\nstopword2')):
            result = load_stopwords('./tests_data/test_stopwords.txt')
            self.assertEqual(result, {'stopword1', 'stopword2'})

    # 测试load_stopwords函数在文件不存在时的行为
    def test_load_stopwords_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = load_stopwords('./tests_data/non_existent_file.txt')
            self.assertEqual(result, set())

    # 测试generate_wordcloud函数是否正确生成词云对象
    def test_generate_wordcloud(self):
        text = 'Hello World'
        font_path = 'simkai.ttf'
        mask = None
        stopwords = set()
        image_color = None
        wc = generate_wordcloud(text, font_path, mask, stopwords, image_color)
        self.assertIsNotNone(wc)

    # 测试save_wordcloud函数是否正确保存词云图像
    def test_save_wordcloud(self):
        # 测试保存词云图函数
        wc = generate_wordcloud('Hello World', 'simkai.ttf', None, set(), None)
        save_wordcloud(wc, 'test_wordcloud', 300, './tests_data/')
        self.assertTrue(os.path.exists('./tests_data/test_wordcloud.png'))

    # 测试beautify_images函数是否正确保存美化的词云图像
    def test_beautify_images(self):
        wc = generate_wordcloud('Hello World', 'simkai.ttf', None, set(), None)
        save_wordcloud(wc, 'test_wordcloud', 300, './tests_data/')
        beautify_images('test_wordcloud', 300, './tests_data/')
        self.assertTrue(os.path.exists('./tests_data/test_wordcloud_beautified.png'))

    # 测试wordcloud_generator函数是否正确生成并保存词云图像
    def test_wordcloud_generator(self):
        # 测试词云图生成器函数
        file_info = {
            'text': self.test_data_path,
            'background': './tests_data/test_background.png'
        }
        save_path = './tests_data/'
        font_path = 'simkai.ttf'
        stopwords = set()
        wordcloud_generator('test_sentiment', file_info, save_path, font_path, stopwords)
        self.assertTrue(os.path.exists('./tests_data/wordcloud_test_sentiment.png'))


if __name__ == '__main__':
    unittest.main()
