# 导入必要的库
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn import metrics
from utils import load_corpus, stopwords, processing


def predict():
    # 设置文件路径
    # TRAIN_PATH = "./data/weibo2018/train.txt"
    # TEST_PATH = "./data/weibo2018/test.txt"

    TRAIN_PATH = "train_texts.csv"
    TEST_PATH = "test_texts.csv"

    # 分别加载训练集和测试集
    train_data = load_corpus(TRAIN_PATH)
    test_data = load_corpus(TEST_PATH)

    # 将训练集和测试集转换为DataFrame
    df_train = pd.DataFrame(train_data, columns=["words", "label"])
    df_test = pd.DataFrame(test_data, columns=["words", "label"])

    # 查看训练集数据（调试）
    print("Training data preview:")
    print(df_train.head())

    # 使用TfidfVectorizer对文本进行向量化
    vectorizer = TfidfVectorizer(token_pattern=r'\[?\w+\]?',
                                 stop_words=stopwords)

    # 转换训练集文本为特征向量
    X_train = vectorizer.fit_transform(df_train["words"])
    y_train = df_train["label"]

    # 转换测试集文本为特征向量
    X_test = vectorizer.transform(df_test["words"])
    y_test = df_test["label"]

    # 使用SVM训练模型
    clf = svm.SVC()
    clf.fit(X_train, y_train)

    # 在测试集上进行预测
    y_pred = clf.predict(X_test)

    # 测试集效果评估
    print("Classification report on test set:")
    print(metrics.classification_report(y_test, y_pred))
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    # 测试自定义文本的分类效果
    strs = ["只要流过的汗与泪都能化作往后的明亮，就值得你为自己喝彩",
            "烦死了！为什么周末还要加班[愤怒]"]

    # 对测试文本进行预处理和向量化
    words = [processing(s) for s in strs]
    vec = vectorizer.transform(words)

    # 预测并输出结果
    output = clf.predict(vec)
    print("Predicted class labels for the input text:")
    print(output)


if __name__ == "__main__":
    predict()
