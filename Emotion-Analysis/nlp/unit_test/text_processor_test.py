import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import csv
from nlp.text_processor import (
    load_scraped_data,
    explain_emojis,
    cut_words,
    rm_url_html,
    rm_punctuation_symbols,
    rm_extra_linebreaks,
    rm_meaningless,
    rm_english_number,
    keep_only_chinese,
    rm_stopwords,
    clean,
    save_to_csv,
    save_words_to_csv,
    text_processor
)
from nlp.stopwords.get_stopwords import get_stopwords


class TestTextProcessor(unittest.TestCase):

    def setUp(self):
        # 创建测试数据和文件
        self.test_csv_path = 'test_weibo_data.csv'
        with open(self.test_csv_path, 'w', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=['id', 'user', 'text'])
            writer.writeheader()
            writer.writerow({'id': 1, 'user': 'user1', 'text': '👍'})

    def tearDown(self):
        # 删除测试文件
        import os
        os.remove(self.test_csv_path)

    def test_load_scraped_data(self):
        data = load_scraped_data(self.test_csv_path)
        self.assertEqual(len(data), 1)

    @patch('emoji.demojize')
    def test_explain_emojis(self, mock_demojize):
        mock_demojize.return_value = '点赞'
        result = explain_emojis('👍')
        self.assertEqual(result, '点赞')

    @patch('jieba.cut')
    def test_cut_words(self, mock_cut):
        mock_cut.return_value = ['This', 'is', 'a', 'test', 'tweet']
        result = cut_words('This is a test tweet')
        self.assertEqual(result, 'This is a test tweet')

    def test_rm_url_html(self):
        text = 'Check out this link: https://www.example.com'
        result = rm_url_html(text)
        self.assertEqual(result, 'Check out this link: ')

    def test_rm_punctuation_symbols(self):
        text = 'Hello, world!'
        result = rm_punctuation_symbols(text)
        self.assertEqual(result, 'Hello world')

    def test_rm_extra_linebreaks(self):
        text = 'Hello\n\nWorld'
        result = rm_extra_linebreaks(text)
        self.assertEqual(result, 'Hello\nWorld')

    def test_rm_meaningless(self):
        text = '# This is a test tweet'
        result = rm_meaningless(text)
        self.assertEqual(result, 'This is a test tweet')

    def test_rm_english_number(self):
        text = 'Hello world 123'
        result = rm_english_number(text)
        self.assertEqual(result, '  ')

    def test_keep_only_chinese(self):
        text = 'Hello world 中国'
        result = keep_only_chinese(text)
        self.assertEqual(result, '中国')

    def test_rm_stopwords(self):
        words = ['的', '是', '测试']
        stopwords = get_stopwords()
        result = rm_stopwords(words)
        self.assertEqual(result, ['测试'])

    def test_clean(self):
        text = 'Hello world 123 https://www.example.com 👍'
        result = clean(text)
        self.assertEqual(result, '拇指向上')

    @patch('nlp.text_processor.process_data')
    def test_text_processor(self, mock_process_data):
        mock_process_data.return_value = ([], [])
        text_processor()
        mock_process_data.assert_called()

    @patch('nlp.text_processor.save_to_csv')
    def test_save_to_csv(self, mock_save):
        save_to_csv([], 'test.csv', ['text'])
        mock_save.assert_called()

    @patch('nlp.text_processor.save_words_to_csv')
    def test_save_words_to_csv(self, mock_save):
        save_words_to_csv(['test'], 'test.csv')
        mock_save.assert_called()


if __name__ == '__main__':
    unittest.main()
