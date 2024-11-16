import json
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wordcloud_generator import beautify_images


def line_chart_generator():
    # 读取文件并解析每行的字典
    data = []
    with (open('../data/emotion_analysis_result.txt', 'r',
               encoding='utf-8-sig')
          as file):
        for line in file:
            data.append(json.loads(line))

    # 存储时间和对应的分数总和
    time_scores = {}

    # 累加分数
    for item in data:
        created_at = item['created_at']
        sentiment_score = item['sentiment_score']
        if created_at in time_scores:
            time_scores[created_at]['total'] += sentiment_score
            time_scores[created_at]['count'] += 1
        else:
            time_scores[created_at] = {'total': sentiment_score, 'count': 1}

    # 计算每个时间的平均分数
    average_scores = {time: scores['total'] / scores['count'] for time, scores
                      in time_scores.items()}

    # 准备绘图数据
    times = list(average_scores.keys())
    scores = list(average_scores.values())

    # 确保时间是有序的
    sorted_indices = sorted(range(len(times)), key=lambda k: times[k])
    times = [times[i] for i in sorted_indices]
    scores = [scores[i] for i in sorted_indices]

    # 创建折线图
    # 设置中文字体
    font_path = 'fonts/NotoSansSC-Regular.ttf'
    font = FontProperties(fname=font_path, size=14)
    plt.figure(figsize=(20, 18), dpi=300)
    plt.plot(times, scores, marker='o', label='平均情感得分')
    # 添加图例
    plt.legend(prop=font)
    # 添加标题和轴标签
    plt.title('情感得分时间曲线图', fontproperties=font)
    plt.xlabel('时间', fontproperties=font)
    plt.ylabel('平均情感得分', fontproperties=font)
    # 显示网格
    plt.grid(True)
    plt.tight_layout(pad=0)
    # 保存
    plt.savefig("../output/line_chart.png", dpi=300)
    beautify_images('line_chart', '../output/')


if __name__ == "__main__":
    line_chart_generator()
