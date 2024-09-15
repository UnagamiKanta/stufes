from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

import json

app = Flask(__name__)

# JSONファイルからデータを読み込む関数
def read_data():
    with open('db.json', 'r') as f:
        data = json.load(f)
    return data

# JSONファイルにデータを書き込む関数
def write_data(data):
    with open('db.json', 'w') as f:
        json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def home():
    data = read_data()
    if request.method == 'POST':
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        try:
            hours = int(hours)
            minutes = int(minutes)
            # 入力値のバリデーション
            if hours < 0:
                hours = 0
            if minutes < 0:
                minutes = 0
            if minutes > 59:
                minutes = 59
            total_minutes = hours * 60 + minutes
            data['currentCoin'] += total_minutes
            data['exp'] += 100 * total_minutes
            write_data(data)
        except ValueError:
            pass  # 数値以外の入力を無視
        return redirect(url_for('home'))
    return render_template('index.html', coin=data['currentCoin'], exp=data['exp'])

# # ホームページ
# @app.route('/')
# def index():
#     return render_template('index.html', current_coin=1000, exp = 100)

# ガチャページへのルート（ガチャページは仮）
@app.route('/gacha')
def gacha():
    return "ガチャページです。"

if __name__ == '__main__':
    app.run(debug=True)