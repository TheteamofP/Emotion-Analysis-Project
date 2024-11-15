from utils import load_corpus, stopwords

TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"

# 分别加载训练集和测试集
train_data = load_corpus(TRAIN_PATH)
test_data = load_corpus(TEST_PATH)

# 将训练集和测试集转换为DataFrame
import pandas as pd
df_train = pd.DataFrame(train_data, columns=["words", "label"])
df_test = pd.DataFrame(test_data, columns=["words", "label"])

# 查看训练集数据（调试）
print("Training data preview:")
print(df_train.head())

# 使用CountVectorizer对文本进行向量化
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer(token_pattern=r'\[?\w+\]?', stop_words=stopwords, max_features=2000)

# 转换训练集文本为特征向量
X_train = vectorizer.fit_transform(df_train["words"])
y_train = df_train["label"]

# 转换测试集文本为特征向量
X_test = vectorizer.transform(df_test["words"])
y_test = df_test["label"]

# 使用XGBoost训练模型
import xgboost as xgb
param = {
    'booster': 'gbtree',
    'max_depth': 6,
    'scale_pos_weight': 0.5,
    'colsample_bytree': 0.8,
    'objective': 'binary:logistic',
    'eval_metric': 'error',
    'eta': 0.3,
    'nthread': 10,
}

# 创建DMatrix
dmatrix_train = xgb.DMatrix(X_train.tocsr(), label=y_train)
model = xgb.train(param, dmatrix_train, num_boost_round=200)

# 在测试集上用模型预测结果
dmatrix_test = xgb.DMatrix(X_test.tocsr())
y_pred = model.predict(dmatrix_test)

# 测试集效果检验
from sklearn import metrics

# 计算AUC
auc_score = metrics.roc_auc_score(y_test, y_pred)
# 将预测概率转换为0/1
y_pred_binary = (y_pred > 0.5).astype(int)

# 打印分类报告和其他指标
print(metrics.classification_report(y_test, y_pred_binary))
print("准确率:", metrics.accuracy_score(y_test, y_pred_binary))
print("AUC:", auc_score)

# 预测自定义文本的情感
from utils import processing

strs = ["哈哈哈哈哈笑死我了", "我也是有脾气的!"]
# 对自定义文本进行处理并向量化
words = [processing(s) for s in strs]
vec = vectorizer.transform(words)

# 转换为DMatrix
dmatrix = xgb.DMatrix(vec)

# 预测并输出结果
output = model.predict(dmatrix)
print("Predicted probabilities:", output)
