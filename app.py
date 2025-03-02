from flask import Flask, render_template,request,session,redirect
from models import db, User 

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# 設定ファイルから設定を読み込む
app.config.from_object("config.Config")

# ルートURLにアクセスしたときの処理を定義
@app.route('/')
def logout():
    # index.htmlテンプレートをレンダリングして返す
    return render_template('index.html')    

# ユーザーリストを表示するURLにアクセスしたときの処理を定義
@app.route('/userlist')
def userlist():
    # dbからユーザーリストを取得
    users = User.query.all()
    # userlist.htmlテンプレートをレンダリングして返す
    return render_template('userlist.html', users=users)

    # ログインURLにアクセスしたときの処理を定義
@app.route('/logon', methods=['GET', 'POST'])
def logon():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # ユーザーが存在するか確認
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # ログイン成功
            session['user_id'] = user.id
            return render_template('showitems.html')
        else:
            # ログイン失敗
            return redirect('/')
    return render_template('index.html')

# ユーザー登録URLにアクセスしたときの処理を定義
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        # ユーザーが既に存在するか確認
        if User.query.filter_by(email=email).first():
            # ユーザーが既に存在する場合
            return redirect('/register')
        else:
            # 新しいユーザーを作成
            new_user = User(email=email, password=password, name=name)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/logon')
    else:
        return render_template('register.html')

# メインモジュールとして実行された場合、アプリケーションを起動
if __name__ == '__main__':
    with app.app_context():  
        # データベースをアプリケーションに初期化    
        db.init_app(app)
        db.create_all() # テーブルを作成

        if not User.query.first():  # 既にデータがある場合は追加しない
            user1 = User(email="user1@example.com", password="password1", name="Buzz")
            user2 = User(email="user2@example.com", password="password2", name="Woody")

            db.session.add_all([user1, user2])  # ユーザーを追加
            db.session.commit()  # データを保存
    app.run(debug=True, use_reloader=False)
