import random  # 导入随机模块，用于随机选取测试样本
import re  # 导入正则表达式模块，用于文本清理
import traceback  # 导入traceback模块，用于异常信息打印

import jieba  # 导入jieba库，用于中文分词
import numpy as np  # 导入numpy库，用于数组操作和数值计算
from sklearn.externals import joblib  # 导入joblib库，用于保存和加载模型
from sklearn.naive_bayes import MultinomialNB  # 导入朴素贝叶斯分类器

# 加载jieba分词字典
jieba.load_userdict("train/word.txt")
# 停用词列表
stop = [line.strip() for line in open('ad/stop.txt', 'r', encoding='utf-8').readlines()]  # 停用词


# 根据词频从文本中提取关键词
def build_key_word(path):  # 通过词频产生特征
    d = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            # 对每一行进行分词
            for word in jieba.cut(line.strip()):
                p = re.compile(r'\w', re.L)  # 正则表达式去掉非字母数字的字符
                result = p.sub("", word)  # 进行字符替换
                if not result or result == ' ':  # 排除空字符
                    continue
                if len(word) > 1:  # 避免单个字符的词语
                    d[word] = d.get(word, 0) + 1  # 统计词频
    # 对所有词进行排序，选择前20%频率最高的词作为关键词
    kw_list = sorted(d, key=lambda x: d[x], reverse=True)
    size = int(len(kw_list) * 0.2)  # 取最前的20%
    mood = set(kw_list[:size])  # 获取关键词集合
    return list(mood - set(stop))  # 去除停用词


# 加载数据集，将微博文本分词，并标记情感标签
def loadDataSet(path):  # 返回每条微博的分词与标签
    line_cut = []  # 存储每条微博分词后的结果
    label = []  # 存储情感标签
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            temp = line.strip()
            try:
                sentence = temp[2:].lstrip()  # 去掉标签前缀，获取微博内容
                label.append(int(temp[:2]))  # 获取微博的情感标签（正面、负面、中性）
                word_list = []
                sentence = str(sentence).replace('\u200b', '')  # 去除零宽度空格
                # 对微博内容进行分词
                for word in jieba.cut(sentence.strip()):
                    p = re.compile(r'\w', re.L)
                    result = p.sub("", word)  # 去掉非字母数字字符
                    if not result or result == ' ':  # 排除空字符
                        continue
                    word_list.append(word)
                # 去除停用词和一些无意义的字符
                word_list = list(set(word_list) - set(stop) - set('\u200b')
                                 - set(' ') - set('\u3000') - set('️'))
                line_cut.append(word_list)
            except Exception:
                continue
    return line_cut, label  # 返回分词后的内容和情感标签


# 将每条微博的词语转换为特征向量
def setOfWordsToVecTor(vocabularyList, moodWords):  # 每条微博向量化
    vocabMarked = [0] * len(vocabularyList)  # 初始化为全0的向量
    for smsWord in moodWords:
        if smsWord in vocabularyList:
            vocabMarked[vocabularyList.index(smsWord)] += 1  # 如果词语在词汇表中，计数加1
    return np.array(vocabMarked)  # 返回转换后的向量


# 将所有微博转换为特征向量
def setOfWordsListToVecTor(vocabularyList, train_mood_array):  # 将所有微博准备向量化
    vocabMarkedList = []
    for i in range(len(train_mood_array)):
        vocabMarked = setOfWordsToVecTor(vocabularyList, train_mood_array[i])  # 转换每条微博
        vocabMarkedList.append(vocabMarked)
    return vocabMarkedList


# 训练朴素贝叶斯模型，计算先验概率和条件概率
def trainingNaiveBayes(train_mood_array, label):  # 计算先验概率
    numTrainDoc = len(train_mood_array)  # 训练文档数量
    numWords = len(train_mood_array[0])  # 单词数量
    prior_Pos, prior_Neg, prior_Neutral = 0.0, 0.0, 0.0  # 初始化先验概率
    # 统计正面、负面、中性情感的微博数量
    for i in label:
        if i == 1:
            prior_Pos = prior_Pos + 1
        elif i == 2:
            prior_Neg = prior_Neg + 1
        else:
            prior_Neutral = prior_Neutral + 1
    prior_Pos = prior_Pos / float(numTrainDoc)  # 正面情感的先验概率
    prior_Neg = prior_Neg / float(numTrainDoc)  # 负面情感的先验概率
    prior_Neutral = prior_Neutral / float(numTrainDoc)  # 中性情感的先验概率

    # 初始化条件概率
    wordsInPosNum = np.ones(numWords)
    wordsInNegNum = np.ones(numWords)
    wordsInNeutralNum = np.ones(numWords)
    PosWordsNum = 2.0  # 设定初始值以避免概率为0
    NegWordsNum = 2.0
    NeutralWordsNum = 2.0

    # 统计各类情感中每个词出现的次数
    for i in range(0, numTrainDoc):
        try:
            if label[i] == 1:
                wordsInPosNum += train_mood_array[i]
                PosWordsNum += sum(train_mood_array[i])  # 正面情感中词汇出现的总次数
            elif label[i] == 2:
                wordsInNegNum += train_mood_array[i]
                NegWordsNum += sum(train_mood_array[i])  # 负面情感中词汇出现的总次数
            else:
                wordsInNeutralNum += train_mood_array[i]
                NeutralWordsNum += sum(train_mood_array[i])  # 中性情感中词汇出现的总次数
        except Exception as e:
            traceback.print_exc(e)  # 输出异常信息
    # 计算条件概率（采用对数以避免计算中的溢出）
    pWordsPosicity = np.log(wordsInPosNum / PosWordsNum)
    pWordsNegy = np.log(wordsInNegNum / NegWordsNum)
    pWordsNeutral = np.log(wordsInNeutralNum / NeutralWordsNum)
    return pWordsPosicity, pWordsNegy, pWordsNeutral, prior_Pos, prior_Neg, prior_Neutral


# 对单条微博进行情感分类
def classify(pWordsPosicity, pWordsNegy, pWordsNeutral, prior_Pos, prior_Neg, prior_Neutral,
             test_word_arrayMarkedArray):
    # 计算每类情感的后验概率
    pP = sum(test_word_arrayMarkedArray * pWordsPosicity) + np.log(prior_Pos)
    pN = sum(test_word_arrayMarkedArray * pWordsNegy) + np.log(prior_Neg)
    pNeu = sum(test_word_arrayMarkedArray * pWordsNeutral) + np.log(prior_Neutral)

    # 比较后验概率，返回情感分类结果
    if pP > pN > pNeu or pP > pNeu > pN:
        return pP, pN, pNeu, 1  # 正面情感
    elif pN > pP > pNeu or pN > pNeu > pP:
        return pP, pN, pNeu, 2  # 负面情感
    else:
        return pP, pN, pNeu, 3  # 中性情感


# 预测所有测试数据的情感分类结果，并计算分类错误率
def predict(test_word_array, test_word_arrayLabel, testCount, PosWords, NegWords, NeutralWords, prior_Pos, prior_Neg,
            prior_Neutral):
    errorCount = 0  # 初始化错误计数
    for j in range(testCount):
        try:
            pP, pN, pNeu, smsType = classify(PosWords, NegWords, NeutralWords, prior_Pos, prior_Neg, prior_Neutral,
                                             test_word_array[j])
            # 如果预测结果与实际标签不一致，则增加错误计数
            if smsType != test_word_arrayLabel[j]:
                errorCount += 1
        except Exception as e:
            traceback.print_exc(e)  # 输出异常信息
    print(errorCount / testCount)  # 输出错误率


if __name__ == '__main__':
    # 执行多次实验，观察结果的变化
    for m in range(1, 11):
        vocabList = build_key_word("train/train.txt")  # 构建词汇表
        line_cut, label = loadDataSet("train/train.txt")  # 加载训练数据
        train_mood_array = setOfWordsListToVecTor(vocabList, line_cut)  # 向量化训练数据
        test_word_array = []  # 测试集
        test_word_arrayLabel = []  # 测试集标签
        testCount = 100  # 从训练集中随机选取100条数据作为测试集
        for i in range(testCount):
            try:
                randomIndex = int(random.uniform(0, len(train_mood_array)))  # 随机选取测试样本
                test_word_arrayLabel.append(label[randomIndex])  # 添加标签
                test_word_array.append(train_mood_array[randomIndex])  # 添加数据
                del (train_mood_array[randomIndex])  # 从训练集中删除选中的样本
                del (label[randomIndex])  # 从标签中删除选中的样本
            except Exception as e:
                print(e)

        # 使用MultinomialNB进行训练和预测
        multi = MultinomialNB()
        multi = multi.fit(train_mood_array, label)  # 训练模型
        joblib.dump(multi, 'model/gnb.model')  # 保存模型
        muljob = joblib.load('model/gnb.model')  # 加载模型
        result = muljob.predict(test_word_array)  # 对测试集进行预测
        count = 0
        for i in range(len(test_word_array)):
            type = result[i]  # 获取预测结果
            if type != test_word_arrayLabel[i]:  # 如果预测结果与实际标签不一致，则增加错误计数
                count = count + 1
            # print(test_word_array[i], "----", result[i])
        print("mul", count / float(testCount))  # 输出错误率

        # 使用自定义朴素贝叶斯进行训练和预测
        PosWords, NegWords, NeutralWords, prior_Pos, prior_Neg, prior_Neutral = \
            trainingNaiveBayes(train_mood_array, label)  # 训练朴素贝叶斯模型
        predict(test_word_array, test_word_arrayLabel, testCount, PosWords, NegWords, NeutralWords, prior_Pos, prior_Neg,
                prior_Neutral)  # 进行预测并计算错误率
