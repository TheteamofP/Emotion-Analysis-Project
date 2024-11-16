from utils import load_corpus_bert
import pandas as pd
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertModel
from sklearn import metrics
import os

# 设置环境变量避免BERT报错
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# 数据路径
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"

# 加载训练集和测试集
train_data = load_corpus_bert(TRAIN_PATH)
test_data = load_corpus_bert(TEST_PATH)

# 将数据转换为DataFrame
df_train = pd.DataFrame(train_data, columns=["text", "label"])
df_test = pd.DataFrame(test_data, columns=["text", "label"])

# BERT模型路径
MODEL_PATH = "./model/chinese_wwm_pytorch"
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
bert = BertModel.from_pretrained(MODEL_PATH)

# 设置设备
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# 超参数
learning_rate = 1e-3
input_size = 768
num_epoches = 10
batch_size = 100
decay_rate = 0.9


# 数据集类
class MyDataset(Dataset):
    def __init__(self, df):
        self.data = df["text"].tolist()
        self.label = df["label"].tolist()

    def __getitem__(self, index):
        data = self.data[index]
        label = self.label[index]
        return data, label

    def __len__(self):
        return len(self.label)


# 创建训练集和测试集DataLoader
train_data = MyDataset(df_train)
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

test_data = MyDataset(df_test)
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


# 测试函数
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
            y_pred.append(outputs)
            y_true.append(labels)

    y_prob = torch.cat(y_pred)
    y_true = torch.cat(y_true)
    y_pred_bin = (y_prob > 0.5).int()  # 将概率转换为二分类标签

    print(metrics.classification_report(y_true, y_pred_bin))
    print("准确率:", metrics.accuracy_score(y_true, y_pred_bin))
    print("AUC:", metrics.roc_auc_score(y_true, y_prob))


# 训练函数
for epoch in range(num_epoches):
    net.train()  # 训练模式
    total_loss = 0

    for i, (words, labels) in enumerate(train_loader):
        tokens = tokenizer(words, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
        input_ids = tokens["input_ids"]
        attention_mask = tokens["attention_mask"]
        labels = labels.float().to(device)

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
    test()

    # 保存模型
    model_path = f"./model/bert_dnn_{epoch + 1}.model"
    torch.save(net.state_dict(), model_path)
    print(f"Saved model: {model_path}")

# 加载最佳模型并进行预测
net.load_state_dict(torch.load("./model/bert_dnn_8.model"))

# 测试自定义文本
s = ["华丽繁荣的城市、充满回忆的小镇、郁郁葱葱的山谷...", "突然就觉得人间不值得"]
tokens = tokenizer(s, padding=True, truncation=True, max_length=128, return_tensors="pt").to(device)
input_ids = tokens["input_ids"]
attention_mask = tokens["attention_mask"]
last_hidden_states = bert(input_ids, attention_mask=attention_mask)
bert_output = last_hidden_states[0][:, 0]  # 获取[CLS] token的输出
outputs = net(bert_output)
print("Predictions for sentences:", outputs)

