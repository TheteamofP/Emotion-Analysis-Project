import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wordcloud_generator import beautify_images


def pie_chart_generator():
    # 读取文件并解析每行的字典
    data = []
    with (open('../data/emotion_analysis_result.txt', 'r',
               encoding='utf-8-sig')
          as file):
        for line in file:
            data.append(json.loads(line))

    # 统计情感极性的数量
    sentiment_counts = {'正面': 0, '负面': 0, '中性': 0}
    for item in data:
        sentiment = item['sentiment']
        if sentiment in sentiment_counts:
            sentiment_counts[sentiment] += 1

    # 准备绘图数据
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    # 为每种情感选择颜色
    colors = ['gold', 'lightcoral', 'lightskyblue']

    # 创建折线图
    # 设置中文字体
    font_path = 'fonts/NotoSansSC-Regular.ttf'
    font = FontProperties(fname=font_path, size=14)
    plt.figure(figsize=(20, 18), dpi=300)
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=140)
    # 添加标题和轴标签
    plt.title('情感极性分布', fontproperties=font)
    plt.axis('equal')  # 使饼图为圆形
    # 保存
    plt.savefig("../output/line_chart.png", dpi=300)
    beautify_images('line_chart', '../output/')


if __name__ == "__main__":
    pie_chart_generator()
