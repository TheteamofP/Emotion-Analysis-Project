import json
import re
import csv
import emoji
import jieba
import unicodedata
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
from bs4 import BeautifulSoup
from datetime import datetime

from stopwords.get_stopwords import get_stopwords
from visualization.logger_config import logger


# import jieba


def load_scraped_data(csv_path, data):
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            # 创建一个csv.DictReader对象
            reader = csv.DictReader(file)
            # 遍历csv文件中的每一行
            for row in reader:
                # 将每一行转换为字典，并添加到列表中
                data.append(row)
            # 打印结果，查看前几行数据
            # for item in data[:5]:
            #     print(item)
            #     print("-" * 50)
    except FileNotFoundError:
        logger.error(f"CSV File {csv_path} not found.")


def explain_emojis(text):
    return emoji.demojize(text, language="zh")


def cut_words(text):
    words = jieba.cut(text, cut_all=False)
    return " ".join(word for word in words if word)


def rm_url_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = re.sub('(http://.*)$', '', text)
    url_regex = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
        r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    return re.sub(url_regex, "", text)


def rm_punctuation_symbols(text):
    return ''.join(ch for ch in text
                   if unicodedata.category(ch)[0] not in ['P', 'S'])


def rm_extra_linebreaks(text):
    lines = text.splitlines()
    return '\n'.join(
        re.sub(r'[\s]+', ' ', l).strip()
        for l in lines if l.strip())


def rm_meaningless(text):
    text = re.sub('[#\n]*', '', text)
    text = text.replace("转发微博", "")
    text = re.sub(r"\s+", " ", text)  # 替换多个空格为一个空格
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)
    return text.strip()


def rm_english_number(text):
    return re.sub(r'[a-zA-Z0-9]+', '', text)


def keep_only_chinese(text):
    # 正则表达式匹配所有中文字符
    chinese_pattern = re.compile(u"[\u4e00-\u9fa5]+")
    # 找到所有匹配的中文字符
    chinese_only = chinese_pattern.findall(text)
    # 将匹配的中文字符连接成一个新的字符串
    return ''.join(chinese_only)


def rm_stopwords(words):
    stopwords = get_stopwords()
    return [word for word in words if word.strip() and word not in stopwords]


def clean(text):
    text = explain_emojis(text)
    text = rm_url_html(text)
    text = rm_punctuation_symbols(text)
    text = rm_extra_linebreaks(text)
    text = rm_meaningless(text)
    text = rm_english_number(text)
    text = keep_only_chinese(text)
    return text.strip()


def text_processor():
    # CSV文件路径
    csv_file_path = '../weibo_crawler/weibo_data.csv'
    # 加载csv爬虫数据文件
    data_list = []
    load_scraped_data(csv_file_path, data_list)

    all_texts = []  # 保存所有文本
    all_words = []  # 保存所有单词
    if data_list:
        for item in data_list:
            if 'text' in item:
                text_value = item['text']
                # 数据清洗
                text_value = clean(text_value)
                # 中文分词
                words = cut_words(text_value).split()
                # 移除停用词
                words = rm_stopwords(words)
                item['text'] = " ".join(words)
                # 保存处理后的文本
                all_texts.append(item['text'])
                # 将处理后的单词添加到 all_words 列表中
                all_words.extend(words)
            else:
                logger.warning(f"The 'text' key is not found in the"
                               f" dictionary.")

            # 删除 'id' 和 'user' 键值对
            item.pop('id', None)  # 使用 pop 来避免 KeyError
            item.pop('user', None)

            # 规范化 'create_at' 时间格式
            if 'create_at' in item:
                # 获取当前日期
                current_date = datetime.now().date()

                # 将当前日期格式化为字符串
                current_date_str = current_date.strftime('%Y-%m-%d')

                original_time = item['create_at']

                if "今天" in original_time or "前" in original_time:
                    formatted_time = current_date_str
                else:
                    try:
                        # 尝试解析时间字符串，至少包含年月日
                        parsed_time = datetime.strptime(original_time,
                                                        '%m-%d')
                        formatted_time = original_time
                    except ValueError:
                        # 解析时间字符串
                        parsed_time = datetime.strptime(original_time,
                                                        '%a %b %d %H'
                                                        ':%M:%S %z %Y')
                        # 格式化时间为年月日
                        formatted_time = parsed_time.strftime('%Y-%m-%d')

                # 更新 'create_at' 为规范化后的时间
                item['create_at'] = formatted_time

    # 打印结果，查看前几行数据
    # for item in data_list[:5]:
    #     print(item)
    #     print("-" * 50)

    # 保存处理后的数据到 CSV 文件
    csv_file_path = '../visualization/processed_data.csv'
    fieldnames = ['keyword', 'region', 'text', 'created_at',
                  'source']
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # 写入数据
        for item in data_list:
            writer.writerow(item)

    # 保存 all_words 为 CSV 文件
    all_words = list(set(all_words))  # 去重
    print(all_words)
    csv_file_path = '../visualization/all_words.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for word in all_words:
            writer.writerow([word])

    # 词汇表
    word_index = {}
    index_word = {}

    for i, word in enumerate(all_words):
        word_index[word] = i
        index_word[i] = word

    # 保存词汇表为 JSON 文件
    json_file_path = '../model/word_index.json'
    with open(json_file_path, 'w', encoding='utf-8-sig') as jsonfile:
        json.dump(word_index, jsonfile, ensure_ascii=False)

    # 将文本转化为整数序列
    sequences = [[word_index[word] for word in text.split()] for text in
                     all_texts]

    # 保存整数序列（可选，用于调试和验证）
    csv_file_path = '../model/sequences.csv'
    with open(csv_file_path, 'w', newline='',
                encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for sequence in sequences:
            writer.writerow(sequence)

    # # 词汇表大小
    # vocab_size = len(word_index)
    # # 嵌入向量的维度
    # embedding_dim = 4
    #
    # # 创建一个Embedding层
    # embedding = nn.Embedding(vocab_size, embedding_dim)
    #
    # # 输入转换为索引
    # input_sequences = [torch.tensor(sequence, dtype=torch.long) for sequence in
    #                    sequences]
    #
    # # 词嵌入
    # embedding_sequences = [embedding(sequence) for sequence in input_sequences]

    # 保存文本、情感标签和情感分数的列表
    sentiment_results = []
    for i, text in enumerate(all_texts):
        sentiment_results.append({
            'text': text,
            'sentiment_label': None,
            'sentiment_score': 0
        })

    # 保存情感分数与文本的字典为 JSON 文件
    json_file_path = '../model/sentiment_results.json'
    with open(json_file_path, 'w', encoding='utf-8-sig') as jsonfile:
        json.dump(sentiment_results, jsonfile, ensure_ascii=False)


if __name__ == "__main__":
    text_processor()






