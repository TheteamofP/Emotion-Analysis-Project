import atexit
import os

from flask import Flask, render_template
from views.page import page
import io
import sys

app = Flask(__name__)

app.register_blueprint(page.pb)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


@app.route('/')
def home():
    return render_template('index.html')


# 定义关闭时执行的函数
def on_flask_shutdown():
    from main import initialization
    # 保存原始目录
    original_dir = os.getcwd()

    initialization(original_dir)


# 注册关闭时执行的函数
atexit.register(on_flask_shutdown)


if __name__ == '__main__':
    app.run()
