import os
import shutil
import subprocess

from weibo_crawler.weibo_crawler.update_settings import main
from nlp.text_processor import text_processor
from model.model_svm import model_svm
from data_visualization.classification import classifcation
from data_visualization.pie_chart_generator import pie_chart_generator
from data_visualization.wordcloud_generator import wordclouds_generator
from data_visualization.question_generator import question_generator


# 改变运行目录并执行对应模块函数
def change_directory_and_execute(original_dir, directory, func, *args, is_scrapy):
    try:
        os.chdir(os.path.join(original_dir, directory))
        func(*args)
        if is_scrapy:
            try:
                subprocess.run(['scrapy', 'crawl', 'search'], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error executing Scrapy command: {e}")
    except Exception as e:
        print(f"Error in {directory}: {e}")
        return False
    finally:
        os.chdir(original_dir)
    return True


def delete_files_in_folder(file_path):
    # 获取绝对路径
    if not os.path.exists(file_path):
        print(f"文件路径不存在：{file_path}")
        return

    try:
        # 检查是文件还是文件夹
        if os.path.isfile(file_path) or os.path.islink(file_path):
            # 删除文件或链接
            os.unlink(file_path)
            print(f"已删除文件：{file_path}")
        elif os.path.isdir(file_path):
            # 如果是文件夹，遍历并删除所有文件
            for filename in os.listdir(file_path):
                file_path_to_delete = os.path.join(file_path, filename)
                if os.path.isfile(file_path_to_delete) or os.path.islink(file_path_to_delete):
                    os.unlink(file_path_to_delete)
                    print(f"已删除文件：{file_path_to_delete}")
    except Exception as e:
        print(f"无法删除 {file_path}：{e}")


# 初始化整个项目
def initialization(original_dir):
    # 清空爬虫配置
    if not change_directory_and_execute(original_dir, 'weibo_crawler',
                                        main, "",
                                        "", '2024-11-16', '2024-11-17',
                                        "", "", "", is_scrapy=False):
        return None

    delete_files_in_folder('data_visualization/all_words.csv')
    delete_files_in_folder('data_visualization/predicted_results.csv')
    delete_files_in_folder('data_visualization/positive_words.csv')
    delete_files_in_folder('data_visualization/negative_words.csv')
    delete_files_in_folder('data_visualization/keywords.csv')
    delete_files_in_folder('data_visualization/regions.csv')
    delete_files_in_folder('data_visualization/sources.csv')
    delete_files_in_folder('data_visualization/dates.csv')
    delete_files_in_folder('model/processed_data.csv')
    delete_files_in_folder('weibo_crawler/weibo_data.csv')

    # 定义源目录和目标目录
    source_dir = os.path.join(original_dir, 'static/wordclouds')
    target_dir = os.path.join(original_dir, 'result')

    # 检查源目录是否存在
    if os.path.exists(source_dir):
        # 检查目标目录是否已存在，如果存在，则先删除
        if os.path.exists(target_dir):
            for filename in os.listdir(source_dir):
                source_file = os.path.join(source_dir, filename)
                target_file = os.path.join(target_dir, filename)

                # 如果目标文件已存在，则重命名新文件
                count = 1
                while os.path.exists(target_file):
                    base, extension = os.path.splitext(target_file)
                    target_file = f"{base}({count}){extension}"
                    count += 1

                # 复制文件
                shutil.copy2(source_file, target_file)
        else:
            # 复制目录
            shutil.copytree(source_dir, target_dir)
        print("Directory copied successfully.")
    else:
        print("Source directory does not exist.")

    delete_files_in_folder('static/wordclouds/pie_chart.png')
    delete_files_in_folder('static/wordclouds/wordcloud_all.png')
    delete_files_in_folder('static/wordclouds/wordcloud_positive.png')
    delete_files_in_folder('static/wordclouds/wordcloud_negative.png')


# 整合调用各个模块
def emotion_analyzer(cookie, keywords, start_date, end_date, regions,
                     weibo_type_input, contain_type_input):
    # 保存原始目录
    original_dir = os.getcwd()

    initialization(original_dir)

    if not change_directory_and_execute(original_dir, 'weibo_crawler',
                                        main, cookie, keywords,
                                        start_date, end_date, regions,
                                        weibo_type_input, contain_type_input,
                                        is_scrapy=True):
        return None

    if not change_directory_and_execute(original_dir, 'nlp',
                                        text_processor, is_scrapy=False):
        return None

    if not change_directory_and_execute(original_dir, 'model',
                                        model_svm, is_scrapy=False):
        return None

    if not change_directory_and_execute(original_dir,
                                        'data_visualization',
                                        classifcation, is_scrapy=False):
        return None

    if not change_directory_and_execute(original_dir,
                                        'data_visualization',
                                        wordclouds_generator, is_scrapy=False):
        return None

    if not change_directory_and_execute(original_dir,
                                        'data_visualization',
                                        pie_chart_generator, is_scrapy=False):
        return None

    if not change_directory_and_execute(original_dir,
                                        'data_visualization',
                                        question_generator, is_scrapy=False):
        return None

    print("Emotion analysis completed successfully")
    return 1


if __name__ == "__main__":
    # 调试测试用
    user_cookie = input("请输入 Cookie: ")
    user_keywords = input("请输入关键词列表，用逗号分隔: ")
    user_start_date = input("请输入搜索的起始日期（格式 yyyy-mm-dd）：")
    user_end_date = input("请输入搜索的终止日期（格式 yyyy-mm-dd）：")
    user_regions = input("请输入想要筛选的微博发布的地区，用逗号分隔：")
    user_weibo_type_input = input("请输入微博类型（全部微博，全部原创微博，"
                                  "热门微博，关注人微博，认证用户微博，媒体微博，观点微博）: ")
    user_contain_type_input = input("请输入筛选类型（不筛选，包含图片，包含视频，包含音乐，包含短链接）: ")

    result = emotion_analyzer(user_cookie, user_keywords, user_start_date,
                              user_end_date, user_regions,
                              user_weibo_type_input, user_contain_type_input)
    if result == 1:
        print("成功！")
    else:
        print("情绪分析未成功完成")
    # # 调试清理
    # original_dir = os.getcwd()
    #
    # initialization(original_dir)
