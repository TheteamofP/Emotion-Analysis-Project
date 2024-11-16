import unittest
from unittest.mock import patch
import os
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
    process_data,
    save_to_csv,
    save_words_to_csv,
    save_word_index_to_json,
    text_processor
)


class TestTextProcessingModule(unittest.TestCase):

    def setUp(self):
        self.test_data_path = 'test_data.csv'
        with open(self.test_data_path, 'w', encoding='utf-8-sig') as f:
            f.write('id,text\n1,Hello World! https://example.com')

    def tearDown(self):
        os.remove(self.test_data_path)

    def test_load_scraped_data(self):
        data = load_scraped_data(self.test_data_path)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['text'], 'Hello World! https://example.com')

    def test_explain_emojis(self):
        text = 'Hello :smile:'
        result = explain_emojis(text)
        self.assertEqual(result, 'Hello 😄')

    def test_cut_words(self):
        text = 'Hello world'
        result = cut_words(text)
        self.assertEqual(result, 'Hello world')

    def test_rm_url_html(self):
        text = 'Hello <b>world</b> https://example.com'
        result = rm_url_html(text)
        self.assertEqual(result, 'Hello world')

    def test_rm_punctuation_symbols(self):
        text = 'Hello, world!'
        result = rm_punctuation_symbols(text)
        self.assertEqual(result, 'Hello world')

    def test_rm_extra_linebreaks(self):
        text = 'Hello\n\nworld'
        result = rm_extra_linebreaks(text)
        self.assertEqual(result, 'Hello world')

    def test_rm_meaningless(self):
        text = '转发微博 #hashtag'
        result = rm_meaningless(text)
        self.assertEqual(result, '')

    def test_rm_english_number(self):
        text = 'Hello123 world'
        result = rm_english_number(text)
        self.assertEqual(result, 'Hello world')

    def test_keep_only_chinese(self):
        text = 'Hello, 世界!'
        result = keep_only_chinese(text)
        self.assertEqual(result, '世界')

    def test_rm_stopwords(self):
        stopwords = {'的', '是'}
        words = ['这是', '一个', '测试', '是', '的']
        result = rm_stopwords(words)
        self.assertEqual(result, ['这是', '一个', '测试'])

    def test_clean(self):
        text = 'Hello, world! https://example.com'
        result = clean(text)
        self.assertEqual(result, 'Hello world')

    def test_process_data(self):
        data = [{'text': 'Hello, world! https://example.com'}]
        all_texts, all_words = process_data(data)
        self.assertEqual(all_texts, ['Hello world'])
        self.assertIn('Hello', all_words)

    def test_save_to_csv(self):
        data = [{'text': 'Hello world'}]
        save_to_csv(data, 'test_output.csv', ['text'])
        self.assertTrue(os.path.exists('test_output.csv'))

    def test_save_words_to_csv(self):
        words = ['Hello', 'world']
        save_words_to_csv(words, 'test_words.csv')
        self.assertTrue(os.path.exists('test_words.csv'))

    def test_save_word_index_to_json(self):
        word_index = {'Hello': 0, 'world': 1}
        save_word_index_to_json(word_index, 'test_word_index.json')
        self.assertTrue(os.path.exists('test_word_index.json'))

    @patch('builtins.print')
    def test_text_processor(self, mock_print):
        text_processor()
        mock_print.assert_called()


if __name__ == '__main__':
    unittest.main()
