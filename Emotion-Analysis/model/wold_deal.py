import pandas as pd
import re
import jieba


# 加载停用词表
def load_stopwords(file_path='stopwords.txt'):
    """
    加载停用词表
    :param file_path: 停用词文件路径，每行一个停用词
    :return: 停用词集合
    """
    stopwords = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
    except FileNotFoundError:
        print(f"Stopwords file not found: {file_path}. Using an empty stopwords list.")
    return stopwords


# 清理文本
def clean_text(text):
    """
    清理文本，移除无用符号、HTML标签和多余空格
    :param text: 输入文本
    :return: 清理后的文本
    """
    # 移除 HTML 标签
    text = re.sub(r'<.*?>', '', text)
    # 移除非中文、字母、数字的字符
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', ' ', text)
    # 移除多余的空格
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# 分词
def tokenize_text(text):
    """
    对文本进行分词
    :param text: 输入文本
    :return: 分词后的字符串
    """
    return ' '.join(jieba.cut(text))


# 去除停用词
def remove_stopwords(text, stopwords):
    """
    去除停用词
    :param text: 分词后的文本
    :param stopwords: 停用词集合
    :return: 去除停用词后的字符串
    """
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)


# 文本预处理主函数
def preprocess_text(text, stopwords):
    """
    对文本进行预处理，包括清理、分词和去除停用词
    :param text: 原始文本
    :param stopwords: 停用词集合
    :return: 预处理后的文本
    """
    text = clean_text(text)
    text = tokenize_text(text)
    text = remove_stopwords(text, stopwords)
    return text


if __name__ == '__main__':
    # 输入和输出文件路径
    input_file = r'D:\PythonProject\EAP\Emotion-Analysis-Project\Emotion-Analysis\weibo_crawler\weibo_data.csv'

    # 读取 CSV 文件
    try:
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
        exit()

    # 检查是否有 text 列
    if 'text' not in df.columns:
        print("Error: Input file does not contain 'text' column.")
        exit()

    # 加载停用词表
    stopwords = load_stopwords()

    # 对 text 列进行预处理
    print("Processing text data...")
    df['text'] = df['text'].apply(lambda x: preprocess_text(str(x), stopwords))

    # 保存结果覆盖原始文件
    print(f"Saving processed data to {input_file}...")
    df.to_csv(input_file, index=False, encoding='utf-8-sig')

    print("Process completed successfully!")
