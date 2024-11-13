import imageio.v2 as imageio
from PIL import Image, ImageEnhance
from matplotlib import pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
# import concurrent.futures
# import jieba
from utils.logger_config import logger  # 导入配置好的logger对象


# 读取文本数据
def load_text_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 未找到。")
        return None


# 中文分词
# def cut_words(text):
#     seg_list = jieba.cut(text, cut_all=False)
#     return " ".join(seg_list)


# 加载停用词列表
def load_stopwords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        logger.error(f"文件 {file_path} 未找到。")
        return set()


# 创建词云图
def generate_wordcloud(text, font_path, mask, stopwords, image_color):
    # if isinstance(mask, Image.Image):
    #     # 将 PIL 图像对象转换为 NumPy 数组
    #     mask = np.array(mask)

    # 楷体：simkai.ttf
    # 隶书：SIMLI.TTF
    # 宋体:simsun.ttc
    # 黑体：simhei.ttf
    # 微软雅黑：msyh.ttc
    wc = WordCloud(
        font_path=font_path,
        background_color="white",       # 设置背景颜色
        color_func=image_color,         # 设置字体颜色,将上面模板图像生成的颜色传入词云
        max_words=250,                  # 最多显示的词数
        max_font_size=250,              # 字体最大值
        min_font_size=30,               # 字体最小值
        random_state=60,                # 设置随机种子以获得可重复的结果
        width=2000, height=1800,        # 设置图片的尺寸
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
    plt.figure(figsize=(20, 18), dpi=dpi)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"{save_path}{filename}.png", dpi=dpi)
    # plt.savefig(f"{save_path}{filename}.pdf", dpi=dpi)  # PDF 格式，无像素化问题


# 美化词云图
def beautify_images(filename, save_path=''):
    image = Image.open(f"{save_path}{filename}.png")

    # 调整图片的对比度、色彩饱和度和锐度
    contrast = 1.1          # 对比度增强10%
    color = 1.1             # 色彩饱和度增强10%
    sharp = 1.3             # 锐度增强30%

    img_contrast = ImageEnhance.Contrast(image).enhance(contrast)
    img_color = ImageEnhance.Color(img_contrast).enhance(color)
    img_sharp = ImageEnhance.Sharpness(img_color).enhance(sharp)
    img_sharp.save(f"{save_path}{filename}_beautified.png")
    # 将美化后的PNG文件保存为PDF格式
    # img_sharp.save(f"{save_path}{filename}_beautified.pdf",
    # "PDF", resolution=dpi)


# 单个文件的词云图生成
def wordcloud_generator(sentiment, file_info, save_path, font_path, stopwords):
    try:
        # 读取文本数据与读取异常处理
        text_data = load_text_data(file_info['text'])
        if text_data is None:
            logger.error(f"未能加载数据文件: {file_info['text']},"
                         f" 中断该文件的词云图生成")
            return

        # # 中文分词
        # words = cut_words(text_data)
        words = text_data

        # 引进背景图片与图片颜色
        bg_image = imageio.imread((file_info['background']))
        bg_image_color = ImageColorGenerator(bg_image)
        # # 将 PIL 图像对象转换为 NumPy 数组
        # bg_image_array = np.array(bg_image)

        # 创建，保存并优化词云图
        wordcloud = generate_wordcloud(words, font_path, bg_image, stopwords,
                                       bg_image_color)
        save_wordcloud(wordcloud, f'wordcloud_{sentiment}', dpi=300,
                       save_path=save_path)
        beautify_images(f'wordcloud_{sentiment}', save_path)
    except Exception as e:
        logger.error(f"生成 {sentiment} 词云图时发生错误: {e}")


# 整体词云图生成器
def wordclouds_generator():
    # 参数data_file
    # 定义文本数据文件路径
    data_files = {
        'positive': {
            'text': '../data/positive_data.csv',
            'background': '../images/wordcloud_backgrounds'
                          '/positive_background.png'
        },
        'negative': {
            'text': '../data/negative_data.csv',
            'background': '../images/wordcloud_backgrounds'
                          '/negative_background.png'
        },
        'neutral': {
            'text': '../data/neutral_data.csv',
            'background': '../images/wordcloud_backgrounds'
                          '/neutral_background.png'
        },
        'all': {
            'text': '../data/preprocess_data.csv',
            'background': '../images/wordcloud_backgrounds/all_background.png'
        }
    }

    # 定义保存和字体路径
    save_path = '../output/wordclouds/'
    font_path = '../static/fonts/NotoSansSC-Regular.ttf'

    # 加载停用词列表
    stopwords = load_stopwords('../static/stopwords/stopwords.txt')
    # 并行生成不同文本数据的词云图
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     for sentiment, file_info in data_files.items():
    #         executor.submit(wordcloud_generator, sentiment, file_info,
    #         save_path, font_path, stopwords)
    for sentiment, file_info in data_files.items():
        wordcloud_generator(sentiment, file_info, save_path, font_path,
                            stopwords)


if __name__ == "__main__":
    wordclouds_generator()
