import unittest
from unittest.mock import patch, mock_open
import csv

from question_generator import (read_text_file, read_csv_file, form_question,
                                load_params)


class TestQuestionGenerator(unittest.TestCase):

    def test_read_text_file_single_line(self):
        # 测试项：确保函数能正确读取单行文本文件内容。
        mock_file_content = "This is a single line"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = read_text_file("dummy_path.txt", False)
        self.assertEqual(result, "This is a single line")

    def test_read_text_file_multiple_lines(self):
        # 测试项：确保函数能正确读取并合并多行文本内容。
        mock_file_content = "Line 1\nLine 2\nLine 3"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = read_text_file("dummy_path.txt", False)
        self.assertEqual(result, "Line 1,Line 2,Line 3")

    def test_read_text_file_file_not_found(self):
        # 测试项：文件不存在时，函数应返回None并打印错误信息。
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = read_text_file("nonexistent_file.txt", False)
        self.assertIsNone(result)

    def test_read_csv_file_with_data(self):
        # 测试项：确保函数能正确解析CSV文件为字典。
        mock_csv_content = "key1,value1\nkey2,value2\nkey3,value3"
        with patch("builtins.open", mock_open(read_data=mock_csv_content)):
            result = read_csv_file("dummy_path.csv")
        self.assertEqual(result, {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        })

    def test_read_csv_file_empty(self):
        # 测试项：CSV文件为空时，函数应返回空字典。
        mock_csv_content = ""
        with patch("builtins.open", mock_open(read_data=mock_csv_content)):
            result = read_csv_file("dummy_path.csv")
        self.assertEqual(result, {})

    def test_read_csv_file_file_not_found(self):
        # 测试项：文件不存在时，函数应返回空字典并打印错误信息。
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = read_csv_file("nonexistent_file.csv")
        self.assertEqual(result, {})

    @patch('question_generator.read_text_file')
    @patch('question_generator.read_csv_file')
    def test_load_params(self, mock_read_csv_file, mock_read_text_file):
        # 模拟 read_text_file 返回值
        mock_read_text_file.side_effect = [
            'all_words_data', 'positive_words_data', 'negative_words_data',
            'keywords_data', 'regions_data', 'sources_data'
        ]

        # 模拟 read_csv_file 返回值
        mock_read_csv_file.side_effect = [
            {'正面': '0.6', '负面': '0.4'},  # sentiment_percentages_data
            {'min_date': '2024-01-01', 'max_date': '2024-12-31'}
            # time_interval_data
        ]

        # 调用 load_params 函数
        result = load_params()

        # 验证返回值
        expected_result = (
            'all_words_data', 'positive_words_data', 'negative_words_data',
            'keywords_data', '2024-01-01 到 2024-12-31', 'regions_data',
            'sources_data', '0.6', '0.4'
        )
        self.assertEqual(result, expected_result)

    def test_form_question_all_params(self):
        # 测试项：所有参数均有值时，确保生成完整的问题描述。
        question = form_question(
            all_words="word1,word2",
            positive_words="pos1,pos2",
            negative_words="neg1,neg2",
            keywords="keyword1,keyword2",
            time_interval="2023-01-01 到 2023-12-31",
            regions="Region1, Region2",
            sources="Source1, Source2",
            positive_percentage="0.75",
            negative_percentage="0.25"
        )
        self.assertIn(
            "整体中文文本数据（词频从大到小前20个或者更少）为'word1,word2",
            question)
        self.assertIn(
            "正面情感中文文本数据（词频从大到小前20个或者更少）为'pos1,pos2",
            question)
        self.assertIn(
            "负面情感中文文本数据（词频从大到小前20个或者更少）为'neg1,neg2",
            question)
        self.assertIn("这些文本数据主要发布于Region1, Region2", question)
        self.assertIn("并且文本数据的来源有'Source1, Source2", question)
        self.assertIn("正面文本数据占整体文本数据的百分比为'0.75'", question)
        self.assertIn("负面文本数据占整体文本数据的百分比为'0.25'", question)

    def test_form_question_missing_params(self):
        # 测试项：部分参数缺失时，确保使用默认文本填充。
        question = form_question(
            all_words=None,
            positive_words=None,
            negative_words=None,
            keywords=None,
            time_interval=None,
            regions=None,
            sources=None,
            positive_percentage=None,
            negative_percentage=None
        )
        self.assertIn("整体中文文本数据为空", question)
        self.assertIn("无正面情感中文文本数据", question)
        self.assertIn("无负面情感中文文本数据", question)
        self.assertIn("这些文本数据发布地区不定未知", question)
        self.assertIn("并且每条数据的来源不定未知", question)
        self.assertIn("正面文本数据占整体的百分比未知", question)
        self.assertIn("负面文本数据占整体的百分比未知", question)


if __name__ == "__main__":
    unittest.main()
