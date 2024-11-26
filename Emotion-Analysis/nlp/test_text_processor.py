import unittest
import csv
import os
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
                             'Hello world!', '2024-11-26 10:00'])

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
        self.assertIn("北京", result)

    def test_rm_url_html(self):
        text = "<div>Hello https://www.example.com</div>"
        result = rm_url_html(text)
        self.assertEqual(result, 'Hello ')

    def test_rm_punctuation_symbols(self):
        text = "Hello, world!"
        result = rm_punctuation_symbols(text)
        self.assertEqual(result, "Hello world")

    def test_rm_extra_linebreaks(self):
        text = "Hello\n\nWorld"
        result = rm_extra_linebreaks(text)
        self.assertEqual(result, "Hello\nWorld")

    def test_rm_meaningless(self):
        text = "#Hello# @user: World"
        result = rm_meaningless(text)
        self.assertEqual(result, 'Hello  World')

    def test_rm_english_number(self):
        text = "Hello123 World 呀"
        result = rm_english_number(text)
        self.assertEqual(result, '  呀')

    def test_keep_only_chinese(self):
        text = "Hello123 World"
        result = keep_only_chinese(text)
        self.assertEqual(result, "")

    def test_rm_stopwords(self):
        words = ["的", "是", "Hello"]
        result = rm_stopwords(words)
        self.assertEqual(result, ["Hello"])

    def test_clean(self):
        text = "<div>世界 Hello https://www.example.com 😊</div>"
        result = clean(text)
        self.assertIn("世界", result)

    def test_process_data(self):
        data = load_scraped_data(self.test_file_path)
        result = process_data(data)
        self.assertEqual(len(result[1]), 1)

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
