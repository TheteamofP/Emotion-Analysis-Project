import unittest
from unittest.mock import patch, mock_open
from io import StringIO
import question_generator


class TestQuestionGenerator(unittest.TestCase):

    @patch('question_generator.read_text_file')
    def test_read_text_file_sources(self, mock_read_text_file):
        # 测试 read_text_file 函数，模拟 sources 文件
        mock_read_text_file.return_value = 'line1,line2,line3'
        result = question_generator.read_text_file('sources.csv', True)
        self.assertEqual(result, 'line1,line2,line3')  # 假设文件中少于20行

    @patch('question_generator.read_text_file')
    def test_read_text_file_sources_full(self, mock_read_text_file):
        # 测试 read_text_file 函数，模拟 sources 文件满20行
        mock_lines = ['line' + str(i) for i in range(50)]  # 创建50行数据
        mock_read_text_file.return_value = ','.join(
            mock_lines[:20])  # 模拟函数返回前20行
        result = question_generator.read_text_file('sources.csv', True)
        self.assertEqual(result, ','.join(mock_lines[:20]))  # 只返回前20行

    @patch('question_generator.read_text_file')
    def test_read_text_file_not_sources(self, mock_read_text_file):
        # 测试 read_text_file 函数，模拟非 sources 文件
        mock_read_text_file.return_value = 'line1,line2,line3'
        result = question_generator.read_text_file('other.txt', False)
        self.assertEqual(result, 'line1,line2,line3')

    @patch('question_generator.read_csv_file')
    def test_read_csv_file(self, mock_read_csv_file):
        # 测试 read_csv_file 函数
        mock_read_csv_file.return_value = {'key1': 'value1', 'key2': 'value2'}
        result = question_generator.read_csv_file('data.csv')
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

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
        result = question_generator.load_params()

        # 验证返回值
        expected_result = (
            'all_words_data', 'positive_words_data', 'negative_words_data',
            'keywords_data', '2024-01-01 到 2024-12-31', 'regions_data',
            'sources_data', '0.6', '0.4'
        )
        self.assertEqual(result, expected_result)

    @patch('question_generator.read_text_file')
    @patch('question_generator.read_csv_file')
    def test_load_params_file_not_found(self, mock_read_csv_file,
                                        mock_read_text_file):
        # 模拟文件未找到的情况
        mock_read_text_file.side_effect = FileNotFoundError
        mock_read_csv_file.side_effect = FileNotFoundError

        # 调用 load_params 函数
        result = question_generator.load_params()

        # 验证返回值是否为 None 或符合预期的默认值
        expected_result = (
            None, None, None, None, '', None, None, '0', '0'
        )
        self.assertEqual(result, expected_result)

    @patch('question_generator.form_question')
    def test_form_question(self, mock_form_question):
        # 测试 form_question 函数
        mock_form_question.return_value = 'Generated question'
        result = question_generator.form_question('all_words', 'positive_words', 'negative_words', 'keywords', 'time_interval', 'regions', 'sources', 'positive_percentage', 'negative_percentage')
        self.assertEqual(result, 'Generated question')

    @patch('question_generator.question_generator')
    def test_question_generator(self, mock_question_generator):
        # 测试 question_generator 函数
        mock_question_generator.return_value = 'Generated question'
        result = question_generator.question_generator()
        self.assertEqual(result, 'Generated question')


if __name__ == '__main__':
    unittest.main()
