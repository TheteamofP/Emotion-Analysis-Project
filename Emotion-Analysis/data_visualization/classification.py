import csv
from data_visualization.logger_config import logger


def classifcation():
    file_path = 'predicted_results.csv'

    # 读取csv文件
    sentiment_results = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            sentiment_results.extend(reader)
    except FileNotFoundError:
        logger.error(f"CSV File {file_path} not found.")

    # 准备三个CSV文件，分别存储正面、负面和中性的情感文本
    csv_files = {
        'positive': 'positive_words.csv',
        'negative': 'negative_words.csv'
    }

    # 确保CSV文件存在
    for filename in csv_files.values():
        open(filename, 'a').close()

    # 根据情感标签将文本写入对应的CSV文件
    for sentiment_result in sentiment_results:
        # 使用get方法获取'sentiment_label'，如果不存在则默认为None
        label = sentiment_result.get('sentiment_label')

        # 使用get方法获取'text'，如果不存在则默认为None
        text = sentiment_result.get('text')

        # 跳过没有标签的情感结果
        if label == '0':
            label = 'negative'
        elif label == '1':
            label = 'positive'
        else:
            continue

        # 跳过空文本
        if not text or not text.strip():
            continue

        if label and text:
            # 将文本按空格分词并写入对应的CSV文件
            with open(csv_files[label], 'a', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile)
                for word in text.split():
                    if word:  # 确保单词不为空
                        writer.writerow([word])

    print("情感文本已根据情感标签分类并保存到CSV文件。")


if __name__ == "__main__":
    classifcation()
