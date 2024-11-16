# 导入必要的库
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from utils import load_corpus, stopwords, processing

# 设置文件路径
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"

# 分别加载训练集和测试集
train_data = load_corpus(TRAIN_PATH)
test_data = load_corpus(TEST_PATH)

# 将训练集和测试集转换为DataFrame
df_train = pd.DataFrame(train_data, columns=["words", "label"])
df_test = pd.DataFrame(test_data, columns=["words", "label"])

# 查看训练集数据
print(df_train.head())

# 使用CountVectorizer对文本进行向量化
vectorizer = CountVectorizer(token_pattern=r'\[?\w+\]?', stop_words=stopwords)

# 转换训练集文本为特征向量
X_train = vectorizer.fit_transform(df_train["words"])
y_train = df_train["label"]

# 转换测试集文本为特征向量
X_test = vectorizer.transform(df_test["words"])
y_test = df_test["label"]

# 使用Multinomial Naive Bayes训练模型
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 使用训练好的模型进行预测
y_pred = clf.predict(X_test)

# 输出测试集效果评估
print(metrics.classification_report(y_test, y_pred))
print("准确率:", metrics.accuracy_score(y_test, y_pred))

# 测试自定义文本的分类效果
strs = ["终于收获一个最好消息", "哭了, 今天怎么这么倒霉"]
# 对测试文本进行处理和转换
words = [processing(s) for s in strs]
vec = vectorizer.transform(words)

# 预测并输出结果
output = clf.predict(vec)
print("预测结果:", output)
