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


if __name__ == '__main__':
    app.run(debug=True)
