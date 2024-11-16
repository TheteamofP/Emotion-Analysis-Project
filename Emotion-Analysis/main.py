import os
import subprocess

from weibo_crawler.weibo_crawler.update_settings import main
from nlp.text_processor import text_processor
from data_visualization.logger_config import logger
from data_visualization.wordcloud_generator import wordclouds_generator


# 改变运行目录并执行对应模块函数
def change_directory_and_execute(original_dir, directory, func, *args, isScrapy):
    try:
        os.chdir(os.path.join(original_dir, directory))
        func(*args)
        if isScrapy:
            try:
                subprocess.run(['scrapy', 'crawl', 'search'], check=True)
            except subprocess.CalledProcessError as e:
                logger.error(f"Error executing Scrapy command: {e}")
    except Exception as e:
        logger.error(f"Error in {directory}: {e}")
        return False
    finally:
        os.chdir(original_dir)
    return True


# 整合调用各个模块
def emotion_analyzer(cookie, keywords, start_date, end_date, regions,
                     weibo_type_input, contain_type_input):
    # 保存原始目录
    original_dir = os.getcwd()

    if not change_directory_and_execute(original_dir, 'weibo_crawler',
                                        main, cookie, keywords,
                                        start_date, end_date, regions,
                                        weibo_type_input, contain_type_input,
                                        isScrapy=True):
        return None

    if not change_directory_and_execute(original_dir, 'nlp',
                                        text_processor,
                                        isScrapy=False):
        return None

    if not change_directory_and_execute(original_dir,
                                        'data_visualization',
                                        wordclouds_generator, isScrapy=False):
        return None

    logger.info("Emotion analysis completed successfully")
    return 1


if __name__ == "__main__":
    # 调试测试用
    user_cookie = input("请输入 Cookie: ")
    user_keywords = input("请输入关键词列表，用逗号分隔: ")
    user_start_date = input("请输入搜索的起始日期（格式 yyyy-mm-dd）：")
    user_end_date = input("请输入搜索的终止日期（格式 yyyy-mm-dd）：")
    user_regions = input("请输入想要筛选的微博发布的地区，用逗号分隔：")
    user_weibo_type_input = input(
        "请输入微博类型（全部微博，全部原创微博，热门微博，关注人微博，认证用户微博"
        "，媒体微博，观点微博）: ")
    user_contain_type_input = input(
        "请输入筛选类型（不筛选，包含图片，包含视频，包含音乐，包含短链接）: ")

    result = emotion_analyzer(user_cookie, user_keywords, user_start_date,
                              user_end_date, user_regions,
                              user_weibo_type_input, user_contain_type_input)
    if result == 1:
        print("成功！")
    else:
        logger.info("情绪分析未成功完成")




