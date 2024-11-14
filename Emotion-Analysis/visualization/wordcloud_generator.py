import imageio.v2 as imageio
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import jieba
from visualization.logger_config import logger


# 读取文本数据
def load_text_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return None


# 中文分词
def cut_words(text):
    return " ".join(jieba.cut(text, cut_all=False))


# 加载停用词列表
def load_stopwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return set()


# 创建词云图
def generate_wordcloud(text, font_path, mask, stopwords, image_color):
    wc = WordCloud(
        font_path=font_path,
        background_color="white",       # 设置背景颜色
        color_func=image_color,         # 设置字体颜色,将上面模板图像生成的颜色传入词云
        max_words=250,                  # 最多显示的词数
        max_font_size=250,              # 字体最大值
        min_font_size=30,               # 字体最小值
        random_state=60,                # 设置随机种子以获得可重复的结果
        width=20, height=18,            # 设置图片的尺寸
        margin=1,                       # 设置词与词之间的距离
        stopwords=stopwords,
        mask=mask,
        prefer_horizontal=1.0,           # 词语横排显示的概率
        scale=3                          # 增加 scale 参数以提高输出图像的分辨率
    )
    return wc.generate(text)


# 保存词云图
def save_wordcloud(wc, filename, dpi, save_path=''):
    # 显式地关闭所有打开的图形
    plt.close('all')
    # 使用Agg后端避免启动GUI
    plt.switch_backend('Agg')
    plt.figure(figsize=(9, 6), dpi=dpi)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"{save_path}{filename}.png", dpi=dpi)


# 美化词云图
def beautify_images(filename, save_path=''):
    image = Image.open(f"{save_path}{filename}.png")

    # 调整图片的对比度、色彩饱和度和锐度
    contrast = 1.3          # 对比度增强30%
    color = 1.3             # 色彩饱和度增强30%
    sharp = 1.5             # 锐度增强50%

    img_contrast = ImageEnhance.Contrast(image).enhance(contrast)
    img_color = ImageEnhance.Color(img_contrast).enhance(color)
    img_sharp = ImageEnhance.Sharpness(img_color).enhance(sharp)
    img_sharp.save(f"{save_path}{filename}.png")


# 单个文件的词云图生成
def wordcloud_generator(sentiment, file_info, save_path, font_path, stopwords):
    try:
        # 读取文本数据与读取异常处理
        words = load_text_data(file_info['text'])
        if words is None:
            logger.error(f"Failed to load data file: {file_info['text']}")
            return

        # 中文分词
        words = cut_words(words)

        # 引进背景图片与图片颜色
        bg_image = imageio.imread((file_info['background']))
        bg_image_color = ImageColorGenerator(bg_image)

        # 创建，保存并优化词云图
        wordcloud = generate_wordcloud(words, font_path, bg_image, stopwords,
                                       bg_image_color)
        save_wordcloud(wordcloud, f'wordcloud_{sentiment}', dpi=150,
                       save_path=save_path)
        beautify_images(f'wordcloud_{sentiment}', save_path)
    except Exception as e:
        logger.error(f"Error generating {sentiment} wordcloud: {e}")


# 整体词云图生成器
def wordclouds_generator():
    # 参数data_file
    # 定义文本数据文件路径
    data_files = {
        'positive': {
            'text': 'data_for_wordcloud.csv',
            'background': 'wordcloud_backgrounds'
                          '/weibo.png'
        },
        'negative': {
            'text': 'data_for_wordcloud.csv',
            'background': 'wordcloud_backgrounds'
                          '/weibo(2).png'
        },
        'neutral': {
            'text': 'data_for_wordcloud.csv',
            'background': 'wordcloud_backgrounds'
                          '/weibo(3).png'
        },
        'all': {
            'text': 'data_for_wordcloud.csv',
            'background': 'wordcloud_backgrounds'
                          '/weibo(4).png'
        }
    }

    # 定义保存和字体路径
    save_path = '../output/wordclouds/'
    font_path = './fonts/NotoSansSC-Regular.ttf'

    # 加载停用词列表
    stopwords = load_stopwords('stopwords/stopwords.txt')

    for sentiment, file_info in data_files.items():
        wordcloud_generator(sentiment, file_info, save_path, font_path,
                            stopwords)


if __name__ == "__main__":
    wordclouds_generator()

# 网页测试
# from flask import Flask, render_template
# from views.page import page
#
# app = Flask(__name__)
#
# app.register_blueprint(page.pb)
#
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# @app.route('/output', methods=['GET'])
# def output():
#     # 你的处理逻辑
#     return "输出内容"
#
# if __name__ == '__main__':
#     app.run()
#
#
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Image Display</title>
# </head>
# <body>
#     <h1>Image from Project</h1>
#     <img src="{{ url_for('static', filename='output/wordclouds/wordcloud_all.png') }}" alt="Image">
#     <img src="{{ url_for('static', filename='output/wordclouds/wordcloud_negative.png') }}" alt="Image">
#     <img src="{{ url_for('static', filename='output/wordclouds/wordcloud_neutral.png') }}" alt="Image">
#     <img src="{{ url_for('static', filename='output/wordclouds/wordcloud_positive.png') }}" alt="Image">
# </body>
# </html>
