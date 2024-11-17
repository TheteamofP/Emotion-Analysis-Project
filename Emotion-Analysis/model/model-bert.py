import os
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
from sklearn import metrics

# 设置环境变量避免BERT报错
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 数据路径
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"
PREDICT_PATH = r"D:\PythonProject\Emotion-Analysis-Project-main\Emotion-Analysis\model\labeled_train_comments.csv"

# 加载数据集
def load_corpus_from_csv(file_path):
    """
    从 CSV 文件中加载评论数据
    :param file_path: CSV 文件路径
    :return: 数据列表，每条数据包含文本和标签
    """
    df = pd.read_csv(file_path)
    texts = df["text"].tolist()
    labels = df.get("label", [None] * len(df)).tolist()
    return texts, labels

# 加载训练集和测试集
print("加载训练集和测试集...")
train_texts, train_labels = load_corpus_from_csv(TRAIN_PATH)
test_texts, test_labels = load_corpus_from_csv(TEST_PATH)
print("数据加载完成！")

# BERT模型路径
MODEL_PATH = "bert-base-chinese"
print("加载BERT模型...")
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
bert = BertModel.from_pretrained(MODEL_PATH)
print("BERT模型加载成功！")

# 设置设备
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(f"使用设备: {device}")

# 超参数
learning_rate = 1e-4
input_size = 768
num_epoches = 5
batch_size = 32
decay_rate = 0.9

# 数据集类
class MyDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __getitem__(self, index):
        return self.texts[index], self.labels[index]

    def __len__(self):
        return len(self.labels)

# 创建训练集和测试集 DataLoader
train_data = MyDataset(train_texts, train_labels)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

test_data = MyDataset(test_texts, test_labels)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)

# 网络结构
class Net(nn.Module):
    def __init__(self, input_size):
        super(Net, self).__init__()
        self.fc = nn.Linear(input_size, 1)  # 全连接层
        self.sigmoid = nn.Sigmoid()  # Sigmoid激活函数

    def forward(self, x):
        out = self.fc(x)
        out = self.sigmoid(out)  # 返回sigmoid激活后的输出
        return out

# 初始化模型
net = Net(input_size).to(device)

# 损失函数和优化器
criterion = nn.BCELoss()
optimizer = torch.optim.Adam(net.parameters(), lr=learning_rate)
scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=decay_rate)

def test():
    net.eval()  # 评估模式
    y_pred, y_true = [], []

    with torch.no_grad():  # 不计算梯度
        for words, labels in test_loader:
            tokens = tokenizer(words, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
            input_ids = tokens["input_ids"]
            attention_mask = tokens["attention_mask"]
            last_hidden_states = bert(input_ids, attention_mask=attention_mask)
            bert_output = last_hidden_states[0][:, 0]  # 获取[CLS] token的输出
            outputs = net(bert_output)  # 前向传播
            y_pred.append(outputs.cpu())
            y_true.append(torch.tensor(labels).float().cpu())

    y_prob = torch.cat(y_pred)
    y_true = torch.cat(y_true)
    y_pred_bin = (y_prob > 0.5).int()  # 将概率转换为二分类标签

    print(metrics.classification_report(y_true, y_pred_bin))
    print("准确率:", metrics.accuracy_score(y_true, y_pred_bin))
    print("AUC:", metrics.roc_auc_score(y_true, y_prob))

def predict_from_csv(file_path):
    """
    从 CSV 文件加载文本并进行预测
    :param file_path: 包含文本的 CSV 文件路径
    :return: DataFrame，包含预测结果
    """
    df = pd.read_csv(file_path)
    texts = df["text"].tolist()

    net.eval()
    predictions = []
    with torch.no_grad():
        for text in texts:
            tokens = tokenizer([text], padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
            input_ids = tokens["input_ids"]
            attention_mask = tokens["attention_mask"]
            last_hidden_states = bert(input_ids, attention_mask=attention_mask)
            bert_output = last_hidden_states[0][:, 0]  # 获取[CLS] token的输出
            outputs = net(bert_output).cpu().numpy().flatten()
            predictions.append(outputs[0])

    df["prediction"] = predictions
    return df

if __name__ == "__main__":
    # 训练模型
    for epoch in range(num_epoches):
        net.train()  # 训练模式
        total_loss = 0

        for i, (words, labels) in enumerate(train_loader):
            tokens = tokenizer(words, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
            input_ids = tokens["input_ids"]
            attention_mask = tokens["attention_mask"]
            labels = torch.tensor(labels).float().to(device)

            optimizer.zero_grad()  # 清零梯度
            last_hidden_states = bert(input_ids, attention_mask=attention_mask)
            bert_output = last_hidden_states[0][:, 0]  # 获取[CLS] token的输出
            outputs = net(bert_output)  # 前向传播
            loss = criterion(outputs.view(-1), labels)  # 计算损失
            total_loss += loss.item()
            loss.backward()  # 反向传播
            optimizer.step()  # 更新梯度

            if (i + 1) % 10 == 0:
                print(f"epoch:{epoch + 1}, step:{i + 1}, loss:{total_loss / 10:.4f}")
                total_loss = 0

        scheduler.step()  # 学习率衰减

        # 每个epoch结束后进行测试
        print(f"Testing after epoch {epoch + 1}:")
        test()

        # 保存模型
        model_path = f"./model/bert_dnn_epoch{epoch + 1}.pth"
        torch.save(net.state_dict(), model_path)
        print(f"Saved model: {model_path}")

    # 从 CSV 文件预测
    predict_df = predict_from_csv(PREDICT_PATH)
    output_path = "./model/predicted_results.csv"
    predict_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Predictions saved to {output_path}")
