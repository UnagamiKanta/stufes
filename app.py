from flask import Flask, render_template, request, redirect, url_for, session
import json
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # セッションを使用するための秘密鍵を設定

# ガチャアイテムの定義
SSR_items = ['ssr_watagashi', 'ssr_kakigori', 'ssr_takoyaki', 'ssr_yakisoba', 'ssr_ringoame',
             'ssr_kasutera', 'ssr_jagabata', 'ssr_banana', 'ssr_senbei', 'ssr_ikayaki']
SR_items = ['sr_watagashi', 'sr_kakigori', 'sr_takoyaki', 'sr_yakisoba', 'sr_ringoame',
            'sr_kasutera', 'sr_jagabata', 'sr_banana', 'sr_senbei', 'sr_ikayaki']
R_items = ['r_watagashi', 'r_kakigori', 'r_takoyaki', 'r_yakisoba', 'r_ringoame',
           'r_kasutera', 'r_jagabata', 'r_banana', 'r_senbei', 'r_ikayaki']
N_items = ['n_watagashi', 'n_kakigori', 'n_takoyaki', 'n_yakisoba', 'n_ringoame',
           'n_kasutera', 'n_jagabata', 'n_banana', 'n_senbei', 'n_ikayaki']

# 確率設定
SSR_probability = 0.04
SR_probability = 0.10
R_probability = 0.30
N_probability = 0.56

# 各アイテムの出現確率
items = SSR_items + SR_items + R_items + N_items
probabilities = (
    [SSR_probability / len(SSR_items)] * len(SSR_items) +
    [SR_probability / len(SR_items)] * len(SR_items) +
    [R_probability / len(R_items)] * len(R_items) +
    [N_probability / len(N_items)] * len(N_items)
)

# JSONファイルからデータを読み込む関数
def read_data():
    with open('db.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# JSONファイルにデータを書き込む関数
def write_data(data):
    with open('db.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

# ガチャ関数
def roll_gacha():
    return random.choices(items, probabilities)[0]

@app.route('/', methods=['GET', 'POST'])
def home():
    data = read_data()
    message = ''
    if request.method == 'POST':
        if 'study_submit' in request.form:
            # 勉強時間入力フォームの処理
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
        elif 'gacha_submit' in request.form:
            # ガチャボタンの処理
            if data['currentCoin'] >= 100:
                data['currentCoin'] -= 100
                obtained_item = roll_gacha()
                data[obtained_item] += 1
                write_data(data)
                # ガチャ結果をセッションに保存
                session['result'] = obtained_item.upper()
                session['image_filename'] = f"{obtained_item}.webp"
                return redirect(url_for('gacha'))
            else:
                message = "コインが足りません"
    return render_template('home.html', coin=data['currentCoin'], exp=data['exp'], message=message)

@app.route('/gacha')
def gacha():
    result = session.pop('result', None)
    image_filename = session.pop('image_filename', None)
    if result and image_filename:
        return render_template('gacha.html', result=result, image_filename=image_filename)
    else:
        # ガチャ結果がない場合はホームにリダイレクト
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
