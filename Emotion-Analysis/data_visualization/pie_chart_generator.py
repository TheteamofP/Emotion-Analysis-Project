import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from data_visualization.wordcloud_generator import beautify_images


def pie_chart_generator():
    # 读取文本数据与读取异常处理
    file_path = 'predicted_results.csv'
    sentiment_results = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            sentiment_results.extend(reader)
    except FileNotFoundError:
        print(f"CSV File {file_path} not found.")
        return  # 文件未找到时直接退出

    try:
        # 统计情感极性的数量
        sentiment_counts = {'正面': 0, '负面': 0}
        for sentiment_result in sentiment_results:
            # 使用get方法获取'sentiment_label'，如果不存在则默认为None
            label = sentiment_result.get('sentiment_label')

            # 跳过没有标签的情感结果
            if label == '0':
                sentiment_counts['负面'] += 1
            elif label == '1':
                sentiment_counts['正面'] += 1
            else:
                continue

        # 计算总数量和百分比
        total = sum(sentiment_counts.values())
        sentiment_percentages = {key: (value / total) * 100 for key, value in sentiment_counts.items()}

        # 准备绘图数据
        labels = list(sentiment_counts.keys())
        sizes = list(sentiment_counts.values())
        # 为每种情感选择颜色
        colors = ['#0786CC', '#B91B1B']  # 柔和的绿色和红色
        explode = [0.05, 0.05]  # 突出显示每个块（稍微分离）

        # 创建饼图
        # 设置中文字体
        font_path = 'fonts/NotoSansSC-Regular.ttf'
        # 测试使用
        # font_path = ('E:/github_repositories/Emotion-Analysis-Project'
        #              '/Emotion-Analysis/data_visualization/fonts'
        #              '/NotoSansSC-Regular.ttf')
        font = FontProperties(fname=font_path, size=14)
        label_font = FontProperties(fname=font_path, size=18)  # 放大标签字体
        percentage_font = FontProperties(fname=font_path, size=16)  # 放大百分比字体
        plt.figure(figsize=(10, 8))  # 调整图表大小
        wedges, texts, autotexts = plt.pie(
            sizes,
            labels=labels,
            colors=colors,
            explode=explode,
            autopct='%1.1f%%',  # 仅显示百分比
            # 显示百分比和具体数量
            startangle=140,
            textprops={'fontproperties': percentage_font, 'fontsize': 12},
            shadow=True  # 添加阴影
        )
        # 设置标题
        plt.title('情感正负性分布情况', fontproperties=font, fontsize=20)

        # 调整标签字体：放大正负面的标签
        for text in texts:
            text.set_fontproperties(label_font)
            text.set_size(18)  # 调整正负面标签字体大小

        # 调整百分比字体
        for autotext in autotexts:
            autotext.set_fontproperties(percentage_font)
            autotext.set_size(16)  # 调整百分比字体大小

        # 使饼图为圆形
        plt.axis('equal')
        # 保存
        output_path = "../static/wordclouds/pie_chart.png"
        # 测试使用
        # output_path = ("E:/github_repositories/Emotion-Analysis-Project"
        #                "/Emotion-Analysis/static/wordclouds/pie_chart.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Pie chart saved at {output_path}")
        beautify_images('pie_chart', '../static/wordclouds/')

        # 存储百分比数据到CSV文件
        csv_output_path = "sentiment_percentages.csv"
        with open(csv_output_path, 'w', newline='',
                  encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Sentiment', 'Percentage'])
            for sentiment, percentage in sentiment_percentages.items():
                writer.writerow([sentiment, round(percentage, 2)])

        print(f"Sentiment percentages saved at {csv_output_path}")

    except Exception as e:
        print(f"Error generating pie_chart: {e}")


if __name__ == "__main__":
    pie_chart_generator()
