import os
import nltk
from nltk.corpus import stopwords as nltk_stopwords


def get_stopwords():
    project_stopwords_path = '../nltk_stopwords'
    nltk.data.path.append(project_stopwords_path)
    # 路径处理
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 stopwords.txt 的绝对路径
    stopwords_path1 = os.path.join(current_dir, 'stopwords.txt')

    try:
        with open(stopwords_path1, 'r', encoding='utf-8-sig') as f:
            file_stopwords = set(f.read().splitlines())
    except FileNotFoundError:
        print("File stopwords.txt not found.")
        file_stopwords = set()

    # 合并去重
    file_stopwords = file_stopwords.union(file_stopwords)
    nltk_stopwords_cn = set(nltk_stopwords.words('chinese'))
    return file_stopwords.union(nltk_stopwords_cn)


if __name__ == "__main__":
    get_stopwords()
