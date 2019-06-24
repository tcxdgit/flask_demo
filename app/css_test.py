from flask_bootstrap import Bootstrap
# from client import Translation
from flask import Flask,render_template,session, redirect, url_for,abort,flash
from forms import Form

app = Flask(__name__)
# print(app)
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Form()

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)