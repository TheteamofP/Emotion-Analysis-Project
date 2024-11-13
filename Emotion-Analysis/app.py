from flask import Flask, render_template
from views.page import page



app = Flask(__name__)

app.register_blueprint(page.pb)

@app.route('/')
def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()
