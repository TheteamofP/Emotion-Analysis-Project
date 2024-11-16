import csv
import imageio.v2 as imageio
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

from data_visualization.logger_config import logger


# 读取文本数据
def load_text_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            return " ".join(row[0] for row in csv.reader(csvfile)).strip()
    except FileNotFoundError:
        logger.error(f"File {file_path} not found.")
        return None


# 创建词云图
def generate_wordcloud(text, font_path, mask, image_color):
    return WordCloud(
        font_path=font_path,
        background_color="white",       # 设置背景颜色
        color_func=image_color,         # 设置字体颜色,将上面模板图像生成的颜色传入词云
        max_words=250,                  # 最多显示的词数
        max_font_size=250,              # 字体最大值
        min_font_size=30,               # 字体最小值
        random_state=60,                # 设置随机种子以获得可重复的结果
        width=20, height=18,            # 设置图片的尺寸
        margin=1,                       # 设置词与词之间的距离
        mask=mask,
        prefer_horizontal=1.0,           # 词语横排显示的概率
        scale=3                          # 增加 scale 参数以提高输出图像的分辨率
    ).generate(text)


# 保存词云图
def save_wordcloud(wc, filename, dpi, save_path=''):
    plt.figure(figsize=(9, 6), dpi=dpi)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"{save_path}{filename}.png", dpi=dpi)


# 美化词云图
def beautify_images(filename, save_path=''):
    image_path = f"{save_path}{filename}.png"
    image = Image.open(image_path)

    # 调整图片的对比度、色彩饱和度和锐度
    # 对比度增强30%
    img_enhanced = ImageEnhance.Contrast(image).enhance(1.3)
    # 色彩饱和度增强30%
    img_enhanced = ImageEnhance.Color(img_enhanced).enhance(1.3)
    # 锐度增强50%
    img_enhanced = ImageEnhance.Sharpness(img_enhanced).enhance(1.5)
    img_enhanced.save(image_path)


# 单个文件的词云图生成
def wordcloud_generator(sentiment, file_info, save_path, font_path):
    # 读取文本数据与读取异常处理
    words = load_text_data(file_info['text'])
    if words is None:
        logger.error(f"Failed to load data file: {file_info['text']}")
        return

    try:
        # 引进背景图片与图片颜色
        bg_image = imageio.imread((file_info['background']))
        bg_image_color = ImageColorGenerator(bg_image)
        # 创建，保存并优化词云图
        wordcloud = generate_wordcloud(words, font_path, bg_image,
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
        'all': {
            'text': 'all_words.csv',
            'background': 'wordcloud_backgrounds/all_background(6).png'
        }
        # ,
        # 'negative': {
        #     'text': 'data_for_wordcloud.csv',
        #     'background': 'wordcloud_backgrounds'
        #                   '/weibo(2).png'
        # },
        # 'neutral': {
        #     'text': 'data_for_wordcloud.csv',
        #     'background': 'wordcloud_backgrounds'
        #                   '/weibo(3).png'
        # },
        # 'positive': {
        #     'text': 'data_for_wordcloud.csv',
        #     'background': 'wordcloud_backgrounds'
        #                   '/weibo(4).png'
        # }
    }

    # 定义保存和字体路径
    save_path = '../static/wordclouds/'
    font_path = 'fonts/NotoSansSC-Regular.ttf'

    for sentiment, file_info in data_files.items():
        wordcloud_generator(sentiment, file_info, save_path, font_path)


if __name__ == "__main__":
    wordclouds_generator()
