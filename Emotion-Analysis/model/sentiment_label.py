import os
from snownlp import SnowNLP
import pandas as pd

# 加载原始评论数据
def load_raw_comments(file_path):
    """
    从文件中加载原始评论数据
    :param file_path: 文本文件路径，每行一个评论
    :return: 评论列表
    """
    comments = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            comment = line.strip()
            if comment:
                comments.append(comment)
    return comments

# 标注情感标签
def label_sentiments(comments):
    """
    使用 SnowNLP 对评论进行情感分析并标注标签
    :param comments: 评论列表
    :return: DataFrame，包含评论和情感标签
    """
    labeled_data = []
    for comment in comments:
        try:
            s = SnowNLP(comment)
            sentiment_score = s.sentiments  # 得到情感得分，范围为 [0, 1]
            print(f"scores : {sentiment_score}")

            # 标注情感标签
            if sentiment_score < 0.6:
                label = 0  # 负面
            elif sentiment_score <= 0.99:
                label = 1  # 中性
            else:
                label = 2  # 正面

            labeled_data.append((comment, label))
        except Exception as e:
            print(f"Error processing comment: {comment}, Error: {e}")

    # 转为 DataFrame
    df = pd.DataFrame(labeled_data, columns=['Comment', 'Sentiment_Label'])
    return df

# 保存标注结果
def save_labeled_data(df, output_path):
    """
    保存标注后的数据到文件
    :param df: 标注后的 DataFrame
    :param output_path: 输出文件路径
    """
    df.to_csv(output_path, index=False, encoding='utf-8')

if __name__ == '__main__':
    # 文件路径设置
    input_file = r'D:\PythonProject\Emotion-Analysis-Project-main\Emotion-Analysis\model\train_texts.csv'  # 原始评论文件路径
    output_file = 'labeled_train_comments.csv'  # 标注结果保存路径

    # 检查文件是否存在
    if not os.path.exists(input_file):
        print(f"Input file not found: {input_file}")
        exit()

    # 加载评论
    print("Loading comments...")
    comments = load_raw_comments(input_file)

    # 进行情感标注
    print("Labeling sentiments...")
    labeled_df = label_sentiments(comments)

    # 保存标注结果
    print(f"Saving labeled data to {output_file}...")
    save_labeled_data(labeled_df, output_file)

    print("Process completed successfully!")
