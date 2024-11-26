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
            next(reader, None)
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


def form_question(all_words, positive_words, negative_words, keywords, time_interval, regions,
                  source, positive_percentage, negative_percentage):
    question = (
        f"根据最近的情感分析结果，我们得到了以下信息：整体中文文本数据（词频从大到小前250个）为'{all_words}'"
        f"，正面情感中文文本数据（词频从大到小前250个）为'{positive_words}'，"
        f"负面情感中文文本数据（词频从大到小前250个）为'{negative_words}'。用户关注的关键词是'{keywords}'，"
        f"收集的时间区间为'{time_interval}'，这些文本数据主要发布于{regions}，并且每条数据的来源是'{source}'"
        f"。正面文本数据占整体的{positive_percentage}%，"
        f"负面文本数据占{negative_percentage}%。请分析这些结果，"
        f"并针对用户关心的关键词'{keywords}'提出相关结论与建议。"
    )
    return question


def question_generator():
    (all_words, positive_words, negative_words, keywords, time_interval,
     regions, sources, positive_percentage, negative_percentage) = (
        load_params())
    question = form_question(all_words, positive_words, negative_words,
                             keywords, time_interval, regions, sources,
                             positive_percentage, negative_percentage)
    print(question)
