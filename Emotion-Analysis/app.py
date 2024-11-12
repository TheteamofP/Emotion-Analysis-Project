# 用户交互模块和部署接口

import os
from flask import Flask
# 导入配置好的logger对象
from logger_config import logger
from utils import wordcloud_generator

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# # 上传.csv文件并生成词云图
# @app.route('/generate', methods=['POST'])
# def generate_wordcloud():
#     if 'file' not in request.files:
#         return "No file part"
#
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file"
#
#     if file and file.filename.endswith('.csv'):
#         # 保存文件到临时目录
#         filename = secure_filename(file.filename)
#         file_path = os.path.join('/path/to/temp', filename)
#         file.save(file_path)
#
#         # 调用词云图生成函数
#         sentiment = request.form.get('sentiment')
#         data_files = {
#             sentiment: {
#                 'text': file_path,
#                 'background': '/path/to/default_background.png'  # 默认背景图片
#             }
#         }
#         wordcloud_generator.wordcloud_generator(sentiment, data_files[sentiment], 'static/wordclouds/', '/path/to/font.ttf', set())
#
#         # 返回词云图的URL
#         return render_template('result.html', image_url='wordclouds/wordcloud_' + sentiment + '.png')
#
#     return "Invalid file type"
#
# # 提供词云图文件
# @app.route('/wordclouds/<filename>')
# def wordcloud(filename):
#     return send_from_directory('static/wordclouds/', filename)


if __name__ == '__main__':
    # 配置logger
    logger.info('应用程序启动')
    # 运行Flask应用
    app.run()
