import re
import csv
import emoji
import jieba
import unicodedata
from bs4 import BeautifulSoup

from nlp.stopwords.get_stopwords import get_stopwords
from data_visualization.logger_config import logger


# 加载爬取数据
def load_scraped_data(csv_path):
    data = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            data.extend(reader)
    except FileNotFoundError:
        logger.error(f"CSV File {csv_path} not found.")
    return data


# 将表情转换为中文
def explain_emojis(text):
    return emoji.demojize(text, language="zh")


# 中文分词
def cut_words(text):
    return " ".join(jieba.cut(text, cut_all=False))


# 清洗url,html
def rm_url_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    url_regex = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)'
        r'(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+'
        r'(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,'
        r'<>?«»“”‘’]))',
        re.IGNORECASE)
    return re.sub(url_regex, "", text)


# 清洗标点符号和符号
def rm_punctuation_symbols(text):
    return ''.join(ch for ch in text if unicodedata.category(ch)[0] not in
                   ['P', 'S'])


# 清洗多余的空行
def rm_extra_linebreaks(text):
    lines = text.splitlines()
    return '\n'.join(re.sub(r'\s+', ' ', line).strip() for line in lines if line.strip())


# 清洗微博评论无意义字符
def rm_meaningless(text):
    text = re.sub('[#\n]*', '', text)
    text = text.replace("转发微博", "")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)
    return text.strip()


# 清洗英文跟数字
def rm_english_number(text):
    return re.sub(r'[a-zA-Z0-9]+', '', text)


# 清洗为只有中文
def keep_only_chinese(text):
    chinese_pattern = re.compile(u"[\u4e00-\u9fa5]+")
    return ''.join(chinese_pattern.findall(text))


# 移除停用词
def rm_stopwords(words):
    stopwords = get_stopwords()
    return [word for word in words if word.strip() and word not in stopwords]


# 数据清洗
def clean(text):
    text = explain_emojis(text)
    text = rm_url_html(text)
    text = rm_punctuation_symbols(text)
    text = rm_extra_linebreaks(text)
    text = rm_meaningless(text)
    text = rm_english_number(text)
    text = keep_only_chinese(text)
    return text.strip()


# 数据预处理
def process_data(data_list):
    # all_texts = []
    all_data = []  # 用于存储所有数据，包括文本和其他键值对
    all_words = set()

    for item in data_list:
        text_value = item.get('text', '')
        text_value = clean(text_value)
        words = rm_stopwords(cut_words(text_value).split())

        item.pop('id', None)
        item.pop('user', None)
        item['sentiment_label'] = None
        item['sentiment_score'] = 0

        cleaned_item = item.copy()  # 创建字典的副本以避免修改原始数据
        cleaned_item['text'] = " ".join(words)
        all_data.append(cleaned_item)  # 存储清理后的数据项
        all_words.update(words)

    return list(all_words), all_data


# 存储整体文本数据字典给情感模型
def save_to_csv(data_list, csv_file_path, fieldnames):
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)


# 存储整体文本数据（已分词版）给词云生成
def save_words_to_csv(words, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for word in words:
            writer.writerow([word])


# 文本预处理
def text_processor():
    csv_file_path = '../weibo_crawler/weibo_data.csv'
    data_list = load_scraped_data(csv_file_path)

    if data_list:
        all_words, all_data = process_data(data_list)

        save_to_csv(all_data, '../model/processed_data.csv',
                    ['keyword', 'region', 'text', 'created_at',
                     'source', 'sentiment_label', 'sentiment_score'])

        save_words_to_csv(all_words, '../data_visualization'
                                     '/all_words.csv')


if __name__ == "__main__":
    text_processor()






