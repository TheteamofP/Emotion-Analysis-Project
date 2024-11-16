import json
import csv


def classifcation(json_file_path):
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8-sig') as jsonfile:
        sentiment_results = json.load(jsonfile)

    # 准备三个CSV文件，分别存储正面、负面和中性的情感文本
    csv_files = {
        'positive': 'positive_texts.csv',
        'negative': 'negative_texts.csv',
        'neutral': 'neutral_texts.csv'
    }

    # 确保CSV文件存在
    for filename in csv_files.values():
        open(filename, 'a').close()

    # 根据情感标签将文本写入对应的CSV文件
    for sentiment_result in sentiment_results:
        label = sentiment_result['sentiment_label']
        text = sentiment_result['text']

        # 跳过没有标签的情感结果
        if label not in csv_files:
            continue

        # 将文本按空格分词并写入对应的CSV文件
        with open(csv_files[label], 'a', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            for word in text.split():
                writer.writerow([word])  # 每个词单独一行

    print("情感文本已根据情感标签分类并保存到CSV文件。")


if __name__ == "__main__":
    json_file_path = '../model/sentiment_results.json'
    classifcation(json_file_path)
