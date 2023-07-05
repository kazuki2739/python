from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
import db, string, random

app = Flask(__name__)

#アップロード先のファイルパスの定数（絶対パス)
# UPLOAD_FOLDER = 'C://Users/kazuki/Desktop/Python/file_upload_sample/static/images'
@app.route("/", methods = ["GET"])
def index():
    msg = request.args.get("msg")

    if msg == None:
        return render_template("index.html")
    else:
        return render_template("index.html", msg = msg)
    
    return render_template("index.html")

@app.route("/", methods = ["POST"])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')

    if db.login(user_name, password):
        session['user'] = True #sessionにキー'user', バリュー:Trueを保存
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes = 1)
        return redirect(url_for('mypage')) #重複実行にならないためにredirect()
    else :
        error = "ログインに失敗しました。"
        input_data = {
            'user_name' : user_name,
            'password' : password
        }
        return render_template("index.html", error = error, data = input_data) #エラー時の入力欄保持

@app.route('/logout')
def logout():
    session.pop('user', None) #sessionの破棄   第二引数でTrueをNoneに変更
    return redirect(url_for('index'))

@app.route('/')
def top_page():
    return render_template('index.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route("/register")
def register_form():
    return render_template("register.html")

@app.route("/register_exe", methods = ["POST"])
def register_exe():
    user_name = request.form.get("username")
    password = request.form.get("password")


if __name__ == "__main__":
    app.run(debug = True)

