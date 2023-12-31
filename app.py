from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import timedelta
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

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
    
    # バリデーションチェック
    if user_name == "":
        error = "ユーザ名が未入力です。"
        return render_template("register.html", error=error, user_name = user_name, password=password)
    if password == "":
        error = "ユーザ名が未入力です。"
        return render_template("register.html", error=error)
    
    count = db.insert_user(user_name, password)
    
    if count == 1:
        msg = "登録が完了しました。"
        return redirect(url_for("mypage", msg=msg))
    else :
        error = "登録に失敗しました。"
        return render_template("register_book.html", error=error)
    
@app.route("/register_book")
def register_book():
    return render_template("register_book.html")

@app.route("/register_book_exe", methods = ["POST"])
def register_book_exe():
    name = request.form.get("name")
    tyosha = request.form.get("tyosha")
    isbn = request.form.get("isbn")
    
    # バリデーションチェック
    if name == "":
        error = "図書名が未入力です。"
        return render_template("register_book.html", error=error, name = name, tyosha = tyosha, isbn = isbn)
    if tyosha == "":
        error = "著者名が未入力です。"
        return render_template("register_book.html", error=error)
    if isbn == "":
        error = "isbnが未入力です。"
        return render_template("register_book.html", error = error)
    
    count = db.insert_book(name, tyosha, isbn)
    
    if count == 1:
        msg = "登録が完了しました。"
        return redirect(url_for("mypage", msg=msg))
    else :
        error = "登録に失敗しました。"
        return render_template("register_book.html", error=error)
    
@app.route('/mypage', methods = ['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))

@app.route('/book_list')
def book_list():
    
    book_list = db.book_list()
    
    return render_template('book_list.html', book_list = book_list)

@app.route('/book_delete')
def book_delete():
    return render_template('book_delete.html')

@app.route('/book_delete_result', methods = ['POST'])
def book_delete_result():
    id = request.form.get('id')
    db.book_delete(id)
    return render_template('book_delete_result.html')

if __name__ == "__main__":
    app.run(debug = True)

