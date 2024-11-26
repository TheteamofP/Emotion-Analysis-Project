import csv
import imageio.v2 as imageio
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator


# 读取文本数据
def load_text_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            # 初始化一个空列表来存储所有行的数据
            text_data = []
            # 使用csv.reader读取CSV文件
            reader = csv.reader(csvfile)
            # 逐行读取CSV文件
            for row in reader:
                try:
                    # 检查行是否有足够的数据
                    if len(row) > 0:
                        # 将第一列的数据添加到列表中
                        text_data.append(row[0])
                except IndexError:
                    print(
                        "Row with missing data encountered and skipped.")
            result_text = " ".join(text_data).strip()
            return result_text
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None


# 创建词云图
def generate_wordcloud(text, font_path, mask, image_color):
    return WordCloud(
        font_path=font_path,
        background_color="white",       # 设置背景颜色
        color_func=image_color,         # 设置字体颜色,将上面模板图像生成的颜色传入词云
        max_words=260,                  # 最多显示的词数
        max_font_size=250,              # 字体最大值
        min_font_size=40,               # 字体最小值
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


# 保存词云图的词汇
def save_top_words(wc, filename, save_path=''):
    # 获取词汇及其频次
    words_freq = wc.words_
    # 去除重复词汇，只保留频次最高的词汇
    unique_words = set(word for word, freq in words_freq.items())
    # 根据频次排序并选择前20个词汇，如果unique_words不足20个，则取所有词汇
    top_words = sorted(unique_words, key=words_freq.get, reverse=True)[
                :20] if len(unique_words) >= 20 else sorted(unique_words,
                                                            key=words_freq.get,
                                                            reverse=True)
    # 将词汇写入文件
    with open(f"{save_path}{filename}.txt", "w", encoding="utf-8-sig") as f:
        for word in top_words:
            f.write(word + "\n")


# 单个文件的词云图生成
def wordcloud_generator(sentiment, file_info, save_path, font_path,
                        save_path_2):
    # 读取文本数据与读取异常处理
    words = load_text_data(file_info['text'])
    if words is None:
        print(f"Failed to load data file: {file_info['text']}")
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
        save_top_words(wordcloud, f'wordcloud_{sentiment}', save_path_2)
    except Exception as e:
        print(f"Error generating {sentiment} wordcloud: {e}")


# 整体词云图生成器
def wordclouds_generator():
    # 参数data_file    # 定义文本数据文件路径
    data_files = {
        'all': {
            'text': 'all_words.csv',
            'background': 'wordcloud_backgrounds/all_background.png'
        }
        ,
        'positive': {
            'text': 'positive_words.csv',
            'background': 'wordcloud_backgrounds/positive_background.png'
        },
        'negative': {
            'text': 'negative_words.csv',
            'background': 'wordcloud_backgrounds/negative_background.png'
        }

    }

    # 定义保存和字体路径
    save_path = '../static/wordclouds/'
    save_path_2 = ''
    font_path = 'fonts/NotoSansSC-Regular.ttf'

    for sentiment, file_info in data_files.items():
        wordcloud_generator(sentiment, file_info, save_path, font_path,
                            save_path_2)


if __name__ == "__main__":
    wordclouds_generator()
