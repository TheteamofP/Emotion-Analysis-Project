import csv


# 从文本文件中读取数据
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # 使用列表推导式将每一行的数据合并为一个列表
            data = [','.join(row) for row in reader]
            # 将所有行的数据用逗号间隔合并成一个字符串
            return ','.join(data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# 从 CSV 文件中读取数据
def read_csv_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            data = {rows[0]: rows[1] for rows in reader}
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return {}


def load_params():
    # 定义文件路径
    file_paths = {
        'all_words': 'wordcloud_all.txt',
        'positive_words': 'wordcloud_positive.txt',
        'negative_words': 'wordcloud_negative.txt',
        'keywords': 'keywords.csv',
        'regions': 'regions.csv',
        'sources': 'sources.csv',
        'sentiment_percentages': 'sentiment_percentages.csv',
        'time_interval': 'dates.csv'
    }

    # 读取所有文本数据
    all_words = read_text_file(file_paths['all_words'])
    positive_words = read_text_file(file_paths['positive_words'])
    negative_words = read_text_file(file_paths['negative_words'])
    keywords = read_text_file(file_paths['keywords'])
    regions = read_text_file(file_paths['regions'])
    sources = read_text_file(file_paths['sources'])

    # 读取 CSV 数据
    sentiment_percentages_data = read_csv_file(
        file_paths['sentiment_percentages'])
    time_interval_data = read_csv_file(
        file_paths['time_interval'])

    # 提取所需的 CSV 数据
    positive_percentage = sentiment_percentages_data.get('正面', '0')
    negative_percentage = sentiment_percentages_data.get('负面', '0')
    # 形成时间区间字符串
    start_date = time_interval_data.get('min_date', '')
    end_date = time_interval_data.get('max_date', '')
    time_interval = f"{start_date} 到 {end_date}"

    return (all_words, positive_words, negative_words, keywords, time_interval,
            regions, sources, positive_percentage, negative_percentage)


def form_question(all_words, positive_words, negative_words, keywords,
                  time_interval, regions, sources, positive_percentage,
                  negative_percentage):
    # 定义默认文本
    default_texts = {
        "all_words": "整体中文文本数据为空",
        "positive_words": "无正面情感中文文本数据",
        "negative_words": "无负面情感中文文本数据",
        "keywords": "用户没有特别关注的关键词",
        "time_interval": "无设定收集的时间区间",
        "regions": "这些文本数据发布地区不定未知",
        "sources": "并且每条数据的来源不定未知",
        "positive_percentage": "正面文本数据占整体的百分比未知",
        "negative_percentage": "负面文本数据占整体的百分比未知",
        "ask": "请分析这些结果，并提出相关结论与建议"
    }

    # 构建问题文本
    question_parts = [
        "根据最近的情感分析结果，我们得到了以下信息：",
    ]

    # 添加所有词汇数据
    if all_words is not None:
        question_parts.append(
            f"整体中文文本数据（词频从大到小前20个或者更少）为'{all_words}，'")
    else:
        question_parts.append(default_texts["all_words"] + ',')

    # 添加正面和负面情感文本数据
    if positive_words is not None:
        question_parts.append(
            f"正面情感中文文本数据（词频从大到小前20个或者更少）为'{positive_words}'，")
    else:
        question_parts.append(default_texts["positive_words"] + ',')

    if negative_words is not None:
        question_parts.append(
            f"负面情感中文文本数据（词频从大到小前20个或者更少）为'{negative_words}'。")
    else:
        question_parts.append(default_texts["negative_words"] + '.')

    # 添加关键词
    if keywords is not None:
        question_parts.append(f"用户关注的关键词是'{keywords}'，")

    # 添加时间区间
    if time_interval is not None:
        question_parts.append(f"收集的时间区间为'{time_interval}'，")

    # 添加地区
    if regions is not None:
        question_parts.append(f"这些文本数据主要发布于{regions}，")

    # 添加数据来源
    if sources is not None:
        question_parts.append(f"并且每条数据的来源是'{sources}'。")

    # 添加正面和负面百分比
    if positive_percentage is not None:
        question_parts.append(f"正面文本数据占整体的{positive_percentage}%，")
    else:
        question_parts.append(default_texts["positive_percentage"] + ',')

    if negative_percentage is not None:
        question_parts.append(f"负面文本数据占{negative_percentage}%。")
    else:
        question_parts.append(default_texts["negative_percentage"] + '.')

    # 结尾
    if keywords is not None:
        question_parts.append(
            f"请分析这些结果，并针对用户关注的关键词'{keywords}'提出相关结论与建议。")

    # 组合所有部分形成最终问题
    question = '\n'.join(question_parts)
    return question


def question_generator():
    (all_words, positive_words, negative_words, keywords, time_interval,
     regions, sources, positive_percentage, negative_percentage) = (
        load_params())
    question = form_question(all_words, positive_words, negative_words,
                             keywords, time_interval, regions, sources,
                             positive_percentage, negative_percentage)
    print(question)


if __name__ == "__main__":
    question_generator()
