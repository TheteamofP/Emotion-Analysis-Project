import pandas as pd
import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import Dataset, DataLoader
from gensim import models
from sklearn import metrics
from utils import load_corpus, stopwords, processing

# 设置文件路径
TRAIN_PATH = "./data/weibo2018/train.txt"
TEST_PATH = "./data/weibo2018/test.txt"
PREDICT_PATH = r"D:\PythonProject\Emotion-Analysis-Project-main\Emotion-Analysis\model\labeled_train_comments.csv"

if __name__ == "__main__":
    # 加载训练集和测试集
    train_data = load_corpus(TRAIN_PATH)
    test_data = load_corpus(TEST_PATH)

    # 将数据转换为 DataFrame
    df_train = pd.DataFrame(train_data, columns=["text", "label"])
    df_test = pd.DataFrame(test_data, columns=["text", "label"])

    # 打印训练数据预览
    print("训练集示例:")
    print(df_train.head())

    # Word2Vec 输入格式：list(word)
    wv_input = df_train['text'].map(lambda s: [w for w in s.split(" ") if w not in stopwords])

    # 训练 Word2Vec 模型
    word2vec = models.Word2Vec(wv_input, vector_size=64, min_count=1, epochs=1000)

    # 打印部分相似词
    print("Most similar words to '你':", word2vec.wv.most_similar("你"))

    # 使用设备判断来选择 CPU 或 GPU
    device = "cuda:0" if torch.cuda.is_available() else "cpu"

    # 超参数设置
    learning_rate = 5e-4
    num_epoches = 5
    batch_size = 100
    embed_size = 64
    hidden_size = 64
    num_layers = 2

    # 定义数据集类
    class MyDataset(Dataset):
        def __init__(self, df):
            self.data = []
            self.label = df["label"].tolist()
            for s in df["text"].tolist():
                vectors = [word2vec.wv[w] for w in s.split(" ") if w in word2vec.wv.key_to_index]
                vectors = torch.Tensor(vectors)
                self.data.append(vectors)

        def __getitem__(self, index):
            return self.data[index], self.label[index]

        def __len__(self):
            return len(self.label)

    # 自定义 batch 处理函数
    def collate_fn(data):
        data.sort(key=lambda x: len(x[0]), reverse=True)  # 按序列长度降序排列
        data_length = [len(sq[0]) for sq in data]
        x = [i[0] for i in data]
        y = [i[1] for i in data]
        data = pad_sequence(x, batch_first=True, padding_value=0)
        return data, torch.tensor(y, dtype=torch.float32), data_length

    # 创建训练集与测试集
    train_data = MyDataset(df_train)
    train_loader = DataLoader(train_data, batch_size=batch_size, collate_fn=collate_fn, shuffle=True)
    test_data = MyDataset(df_test)
    test_loader = DataLoader(test_data, batch_size=batch_size, collate_fn=collate_fn, shuffle=False)

    # 定义 LSTM 模型
    class LSTM(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers):
            super(LSTM, self).__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
            self.fc = nn.Linear(hidden_size * 2, 1)
            self.sigmoid = nn.Sigmoid()

        def forward(self, x, lengths):
            h0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)
            c0 = torch.zeros(self.num_layers * 2, x.size(0), self.hidden_size).to(device)
            packed_input = torch.nn.utils.rnn.pack_padded_sequence(input=x, lengths=lengths, batch_first=True)
            packed_out, (h_n, h_c) = self.lstm(packed_input, (h0, c0))
            lstm_out = torch.cat([h_n[-2], h_n[-1]], 1)
            out = self.fc(lstm_out)
            out = self.sigmoid(out)
            return out

    # 实例化模型
    lstm = LSTM(embed_size, hidden_size, num_layers).to(device)

    # 定义损失函数与优化器
    criterion = nn.BCELoss()
    optimizer = torch.optim.Adam(lstm.parameters(), lr=learning_rate)

    # 测试函数
    def test():
        lstm.eval()
        y_pred, y_true = [], []
        with torch.no_grad():
            for x, labels, lengths in test_loader:
                x = x.to(device)
                outputs = lstm(x, lengths)
                outputs = outputs.view(-1)
                y_pred.append(outputs)
                y_true.append(labels)

        y_prob = torch.cat(y_pred)
        y_true = torch.cat(y_true)
        y_pred_bin = (y_prob > 0.5).int()

        print(metrics.classification_report(y_true, y_pred_bin))
        print("准确率:", metrics.accuracy_score(y_true, y_pred_bin))
        print("AUC:", metrics.roc_auc_score(y_true, y_prob))

    # 训练过程
    for epoch in range(num_epoches):
        lstm.train()
        total_loss = 0
        for i, (x, labels, lengths) in enumerate(train_loader):
            x = x.to(device)
            labels = labels.to(device)
            outputs = lstm(x, lengths)
            logits = outputs.view(-1)
            loss = criterion(logits, labels)
            total_loss += loss.item()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if (i + 1) % 10 == 0:
                print(f"epoch:{epoch + 1}, step:{i + 1}, loss:{total_loss / 10}")
                total_loss = 0

        # 测试并保存模型
        test()
        model_path = f"./model/lstm_{epoch + 1}.model"
        torch.save(lstm.state_dict(), model_path)
        print(f"Saved model: {model_path}")

    # 从 CSV 文件预测
    predict_df = pd.read_csv(PREDICT_PATH)

    if "text" not in predict_df.columns:
        raise ValueError("CSV 文件中必须包含 'text' 列")

    predict_texts = []
    for s in predict_df["text"].apply(processing).tolist():
        vectors = [word2vec.wv[w] for w in s.split(" ") if w in word2vec.wv.key_to_index]
        predict_texts.append(torch.Tensor(vectors))

    x, _, lengths = collate_fn(list(zip(predict_texts, [-1] * len(predict_texts))))
    x = x.to(device)
    outputs = lstm(x, lengths)
    outputs = outputs.view(-1).tolist()

    predict_df["prediction"] = outputs
    output_path = "./data/weibo2018/predicted_results.csv"
    predict_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"预测结果已保存到: {output_path}")