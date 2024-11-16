import nltk
from nltk.corpus import stopwords as nltk_stopwords

from data_visualization.logger_config import logger


def get_stopwords():
    nltk.download('stopwords')
    try:
        with open('stopwords.txt', 'r', encoding='utf-8-sig') as f:
            file_stopwords = set(f.read().splitlines())

        # 获取NLTK库中的中文停用词
        nltk_stopwords_cn = set(nltk_stopwords.words('chinese'))

        # 合并文件中的停用词和NLTK库中的中文停用词
        all_stopwords = file_stopwords.union(nltk_stopwords_cn)
        return all_stopwords
    except FileNotFoundError:
        logger.error(f"File stopwords.txt not found.")
        # 如果文件不存在，则只返回NLTK库中的中文停用词
        return set(nltk_stopwords.words('chinese'))


if __name__ == "__main__":
    get_stopwords()
