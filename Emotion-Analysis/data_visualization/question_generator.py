import csv
import os


# 从文本文件中读取数据
def read_text_file(file_path, isSources):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # 使用列表推导式将每一行的数据合并为一个列表
            data = [','.join(row) for row in reader]
            # 将所有行的数据用逗号间隔合并成一个字符串
            if isSources:
                return ','.join(data[:20]) if len(data) >= 20 else ','.join(
                    data)
            else:
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = {
        'all_words': os.path.join(current_dir, 'wordcloud_all.txt'),
        'positive_words': os.path.join(current_dir, 'wordcloud_positive.txt'),
        'negative_words': os.path.join(current_dir, 'wordcloud_negative.txt'),
        'keywords': os.path.join(current_dir, 'keywords.csv'),
        'regions': os.path.join(current_dir, 'regions.csv'),
        'sources': os.path.join(current_dir, 'sources.csv'),
        'sentiment_percentages': os.path.join(current_dir,
                                              'sentiment_percentages.csv'),
        'time_interval': os.path.join(current_dir, 'dates.csv')
    }

    # 读取所有文本数据
    all_words = read_text_file(file_paths['all_words'], False)
    positive_words = read_text_file(file_paths['positive_words'], False)
    negative_words = read_text_file(file_paths['negative_words'], False)
    keywords = read_text_file(file_paths['keywords'], False)
    regions = read_text_file(file_paths['regions'], False)
    sources = read_text_file(file_paths['sources'], True)

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
        "all_words": "\n整体中文文本数据为空",
        "positive_words": "\n无正面情感中文文本数据",
        "negative_words": "\n无负面情感中文文本数据",
        "keywords": "\n用户没有特别关注的关键词",
        "time_interval": "\n无设定收集的时间区间",
        "regions": "\n这些文本数据发布地区不定未知",
        "sources": "\n并且每条数据的来源不定未知",
        "positive_percentage": "\n正面文本数据占整体的百分比未知",
        "negative_percentage": "\n负面文本数据占整体的百分比未知"
    }

    # 构建问题文本
    question_parts = [
        "根据最近的情感分析结果，我们得到了以下信息：",
    ]

    # 添加所有词汇数据
    if all_words is not None:
        question_parts.append(
            f"\n整体中文文本数据（词频从大到小前20个或者更少）为'{all_words}，'")
    else:
        question_parts.append(default_texts["all_words"] + ',')

    # 添加正面和负面情感文本数据
    if positive_words is not None:
        question_parts.append(
            f"\n正面情感中文文本数据（词频从大到小前20个或者更少）为'{positive_words}'，")
    else:
        question_parts.append(default_texts["positive_words"] + ',')

    if negative_words is not None:
        question_parts.append(
            f"\n负面情感中文文本数据（词频从大到小前20个或者更少）为'{negative_words}'。")
    else:
        question_parts.append(default_texts["negative_words"] + '。')

    # 添加关键词
    if keywords is not None:
        question_parts.append(f"\n用户关注的关键词是'{keywords}'，")
    else:
        question_parts.append(default_texts["keywords"] + '，')

    # 添加时间区间
    if time_interval is not None:
        question_parts.append(f"收集的时间区间为'{time_interval}'，")
    else:
        question_parts.append(default_texts["time_interval"] + '。')

    # 添加地区
    if regions is not None:
        question_parts.append(f"\n这些文本数据主要发布于{regions}，")
    else:
        question_parts.append(default_texts["regions"] + ',')

    # 添加数据来源
    if sources is not None:
        question_parts.append(f"并且文本数据的来源有'{sources}'。")
    else:
        question_parts.append(default_texts["sources"] + '。')

    # 添加正面和负面百分比
    if positive_percentage is not None:
        question_parts.append(f"\n正面文本数据占整体文本数据的百分比为'{positive_percentage}'，")
    else:
        question_parts.append(default_texts["positive_percentage"] + '，')

    if negative_percentage is not None:
        question_parts.append(f"负面文本数据占整体文本数据的百分比为'{negative_percentage}'。")
    else:
        question_parts.append(default_texts["negative_percentage"] + '。')

    # 组合所有部分形成最终问题
    question = '\n<br>'.join(question_parts)
    print(question)
    return question


def question_generator():
    (all_words, positive_words, negative_words, keywords, time_interval,
     regions, sources, positive_percentage, negative_percentage) = (
        load_params())
    question = form_question(all_words, positive_words, negative_words,
                             keywords, time_interval, regions, sources,
                             positive_percentage, negative_percentage)
    print(question)

    return question


if __name__ == "__main__":
    question_generator()
