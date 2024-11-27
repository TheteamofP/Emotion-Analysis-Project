import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import metrics
from model.utils import load_corpus, stopwords, processing

# 文件路径
TRAIN_PATH = "weibo2018/train.txt"
TEST_PATH = "weibo2018/test.txt"
PREDICT_PATH = r"processed_data.csv"


def model_svm():
    # 加载训练集和测试集
    train_data = load_corpus(TRAIN_PATH)
    test_data = load_corpus(TEST_PATH)

    # 将训练集和测试集转换为 DataFrame
    df_train = pd.DataFrame(train_data, columns=["words", "label"])
    df_test = pd.DataFrame(test_data, columns=["words", "label"])

    # 查看训练集数据
    print("训练集示例:")
    print(df_train.head())

    # 使用 TfidfVectorizer 对文本进行向量化
    vectorizer = TfidfVectorizer(token_pattern=r'\[?\w+\]?',
                                 stop_words=stopwords)

    # 转换训练集文本为特征向量
    X_train = vectorizer.fit_transform(df_train["words"])
    y_train = df_train["label"]

    # 转换测试集文本为特征向量
    X_test = vectorizer.transform(df_test["words"])
    y_test = df_test["label"]

    # 使用 SVM 训练模型
    clf = svm.SVC()
    clf.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = clf.predict(X_test)

    # 输出测试集效果评估
    print("测试集分类报告:")
    print(metrics.classification_report(y_test, y_pred))
    print("准确率:", metrics.accuracy_score(y_test, y_pred))

    # 从 CSV 文件加载预测文本
    predict_df = pd.read_csv(PREDICT_PATH)

    # 确保测试文本列存在并进行预处理
    if "text" not in predict_df.columns:
        raise ValueError("CSV 文件中必须包含 'text' 列")

    predict_texts = predict_df["text"].apply(processing).tolist()

    # 转换测试文本为特征向量
    vec = vectorizer.transform(predict_texts)

    # 预测并输出结果
    predictions = clf.predict(vec)
    # 保存情感分数
    predict_df["sentiment_score"] = predictions
    # 保存情感标签
    predict_df["sentiment_label"] = (predictions > 0.5).astype(int)

    # 保存预测结果到 CSV 文件
    output_path = "../data_visualization/predicted_results.csv"
    predict_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"预测结果已保存到: {output_path}")


if __name__ == "__main__":
    model_svm()
