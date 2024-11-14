import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from datasets import load_dataset
from sklearn.metrics import accuracy_score, classification_report

# 1. 加载IMDB数据集
dataset = load_dataset("imdb")

# 2. 加载BERT预训练模型和Tokenizer
model_name = "bert-base-uncased"  # 使用BERT基础模型（英文）
tokenizer = BertTokenizer.from_pretrained(model_name)


# 3. 数据预处理（tokenize文本数据）
def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)


# 对训练集和测试集进行处理
encoded_dataset = dataset.map(preprocess_function, batched=True)

# 4. 将数据集分割为训练集和测试集
train_dataset = encoded_dataset["train"].shuffle(seed=42).select([i for i in list(range(3000))])  # 仅使用前3000条数据来加快训练速度
test_dataset = encoded_dataset["test"].shuffle(seed=42).select([i for i in list(range(1000))])  # 仅使用前1000条数据来加快测试速度


# 5. 转换为PyTorch Dataset格式
class IMDBDataset(torch.utils.data.Dataset):
    def __init__(self, encoded_data):
        self.data = encoded_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.data.items()}
        return item


train_dataset = IMDBDataset(train_dataset)
test_dataset = IMDBDataset(test_dataset)

# 6. 创建DataLoader
train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=8)

# 7. 加载BERT模型用于文本分类
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

# 8. 编译模型
optimizer = AdamW(model.parameters(), lr=2e-5)


# 9. 训练模型
def train(model, dataloader, optimizer):
    model.train()
    total_loss = 0
    for batch in dataloader:
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['label'].to(device)

        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
    avg_loss = total_loss / len(dataloader)
    return avg_loss


# 训练模型3轮
for epoch in range(3):
    train_loss = train(model, train_dataloader, optimizer)
    print(f"Epoch {epoch + 1}: Training loss = {train_loss}")


# 10. 评估模型
def evaluate(model, dataloader):
    model.eval()
    predictions, true_labels = [], []
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['label'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=1)

            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

    return predictions, true_labels


# 获取测试集上的预测和真实标签
predictions, true_labels = evaluate(model, test_dataloader)

# 计算准确率和分类报告
print("Accuracy:", accuracy_score(true_labels, predictions))
print(classification_report(true_labels, predictions))


# 11. 模型推理（预测新的文本）
def predict_sentiment(text):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding="max_length", truncation=True, max_length=512).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class = torch.argmax(logits, dim=1).cpu().numpy()[0]
    sentiment = "Positive" if predicted_class == 1 else "Negative"
    return sentiment


# 测试推理
print(predict_sentiment("I love this movie! It was amazing!"))
print(predict_sentiment("I hate this movie. It was terrible."))
