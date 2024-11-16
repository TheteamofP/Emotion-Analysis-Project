import os

import nltk
from nltk.corpus import stopwords as nltk_stopwords

from data_visualization.logger_config import logger


def get_stopwords():
    nltk.download('stopwords')
    # 路径处理
    # original_dir = os.getcwd()
    # os.chdir(os.path.join(original_dir, 'stopwords'))

    try:
        with open('stopwords.txt', 'r', encoding='utf-8-sig') as f:
            file_stopwords = set(f.read().splitlines())
    except FileNotFoundError:
        logger.error("File stopwords.txt not found.")
        file_stopwords = set()

    # 合并去重
    nltk_stopwords_cn = set(nltk_stopwords.words('chinese'))
    return file_stopwords.union(nltk_stopwords_cn)


if __name__ == "__main__":
    get_stopwords()
