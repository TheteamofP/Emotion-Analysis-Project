import unittest
import csv
import os
from datetime import datetime
from text_processor import (load_scraped_data, explain_emojis, cut_words,
                            rm_url_html, rm_punctuation_symbols,
                            rm_extra_linebreaks, rm_meaningless,
                            rm_english_number, keep_only_chinese, rm_stopwords,
                            clean, process_data, save_to_csv,
                            save_words_to_csv, text_processor)

FILE_DIR = ("E:/github_repositories/Emotion-Analysis-Project/Emotion-Analysis"
            "/nlp/test_utils")


class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        # 创建测试文件和目录
        self.test_file_path = FILE_DIR + 'test_weibo_data.csv'
        self.date_file_path = FILE_DIR + 'test_dates.csv'
        with open(self.test_file_path, 'w', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'user', 'keyword', 'region', 'source',
                             'text', 'created_at'])
            writer.writerow(['1', 'user1', 'keyword1', 'region1', 'source1',
                             '我爱北京天安门', '2024-11-26 10:00'])

    def tearDown(self):
        # 删除测试文件
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
        if os.path.exists(self.date_file_path):
            os.remove(self.date_file_path)
        if os.path.exists('test_processed_data.csv'):
            os.remove('test_processed_data.csv')
        if os.path.exists('test_all_words.csv'):
            os.remove('test_all_words.csv')
        if os.path.exists('test_keywords.csv'):
            os.remove('test_keywords.csv')
        if os.path.exists('test_regions.csv'):
            os.remove('test_regions.csv')
        if os.path.exists('test_sources.csv'):
            os.remove('test_sources.csv')

    def test_load_scraped_data(self):
        data = load_scraped_data(self.test_file_path)
        self.assertEqual(len(data), 1)

    def test_explain_emojis(self):
        text = "😊"
        result = explain_emojis(text)
        self.assertIn(":羞涩微笑:", result)

    def test_cut_words(self):
        text = "我爱北京天安门"
        result = cut_words(text)
        # 检查结果是否包含"北京"并且是以空格分隔的分词结果
        self.assertIn("北京", result)
        # 检查结果是否包含"天安门"并且是以空格分隔的分词结果
        self.assertIn("天安门", result)
        # 检查结果是否包含"我"和"爱"并且是以空格分隔的分词结果
        self.assertIn("我", result)
        self.assertIn("爱", result)
        # 检查结果是否包含空格分隔的四个词
        words = result.split()
        self.assertEqual(len(words), 4)

    def test_rm_url_html(self):
        text = "<div>Hello https://www.example.com</div>"
        result = rm_url_html(text)
        self.assertEqual(result, 'Hello ')

    def test_rm_punctuation_symbols(self):
        text = "你好, 世界@#￥%……&*!"
        result = rm_punctuation_symbols(text)
        self.assertEqual(result, "你好 世界")

    def test_rm_extra_linebreaks(self):
        text = "Hello\n\n\n\n\n\nWorld\n\n\n"
        result = rm_extra_linebreaks(text)
        self.assertEqual(result, "Hello\nWorld")

    def test_rm_meaningless(self):
        text = "#超话标题# @double_t: 世界"
        result = rm_meaningless(text)
        self.assertEqual(result, '超话标题  世界')

    def test_rm_english_number(self):
        text = "Hello123 World 呀"
        result = rm_english_number(text)
        self.assertEqual(result, '  呀')

    def test_keep_only_chinese(self):
        text = "你好こんにちは하세요"
        result = keep_only_chinese(text)
        self.assertEqual(result, "你好")

    def test_rm_stopwords(self):
        words = ["哎呀", "也是", "几乎", "我也是服了"]
        result = rm_stopwords(words)
        self.assertEqual(result, ["我也是服了"])

    def test_clean(self):
        text = ("<div>#超话# @double_t: こんにちは하세요 Hello123 "
                "@#￥%……&*! https://www.example.com 😊世界\n\n\n\n\n\n"
                "你好\n\n\n\n\n\n</div>")
        result = clean(text)
        self.assertIn("超话世界你好", result)

    def test_process_data(self):
        # 加载测试数据
        data = load_scraped_data(self.test_file_path)
        # 处理数据
        result = process_data(data)
        # 验证返回的元组长度是否正确
        self.assertEqual(len(result), 7)
        # 验证处理后的数据列表长度是否为1（假设测试数据只有一条记录）
        self.assertEqual(len(result[1]), 1)
        # 验证返回的all_words是否为列表
        self.assertIsInstance(result[0], list)
        # 验证返回的keywords是否为列表
        self.assertIsInstance(result[2], list)
        # 验证返回的regions是否为列表
        self.assertIsInstance(result[3], list)
        # 验证返回的sources是否为列表
        self.assertIsInstance(result[4], list)
        # 验证返回的min_date是否为datetime对象或None
        self.assertIsInstance(result[5], (datetime, type(None)))
        # 验证返回的max_date是否为datetime对象或None
        self.assertIsInstance(result[6], (datetime, type(None)))
        # 验证处理后的数据项是否包含正确的字段
        cleaned_item = result[1][0]
        self.assertIn('text', cleaned_item)
        self.assertIn('sentiment_label', cleaned_item)
        self.assertIn('sentiment_score', cleaned_item)
        # 验证文本是否经过清洗和分词，我在停用词列表中
        expected_text = cut_words(clean("爱北京天安门"))
        self.assertEqual(cleaned_item['text'], expected_text)

    def test_save_to_csv(self):
        data = [{"text": "Hello"}]
        save_to_csv(data, 'test_processed_data.csv', ['text'])
        self.assertTrue(os.path.exists('test_processed_data.csv'))

    def test_save_words_to_csv(self):
        words = ["Hello"]
        save_words_to_csv(words, 'test_all_words.csv')
        self.assertTrue(os.path.exists('test_all_words.csv'))

    def test_text_processor(self):
        text_processor()
        self.assertTrue(os.path.exists('E:/github_repositories'
                                       '/Emotion-Analysis-Project'
                                       '/Emotion-Analysis/data_visualization'
                                       '/dates.csv'))


if __name__ == '__main__':
    unittest.main()
