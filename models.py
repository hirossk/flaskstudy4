from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ユーザーモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    email = db.Column(db.String(120), unique=True, nullable=False)  # ユニークなメールアドレス
    password = db.Column(db.String(60), nullable=False)  # パスワード
    name = db.Column(db.String(100), nullable=False)  # 名前

    def check_password(self, password):
        # 指定されたパスワードがユーザーのパスワードと一致するかを確認します。
        # Args:
        #    password (str): 確認するパスワード。
        #Returns:
        #    bool: パスワードが一致する場合はTrue、一致しない場合はFalse
        return self.password == password

# アイテムモデル
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    code = db.Column(db.Integer, unique=True, nullable=False)  # ユニークなコード
    name = db.Column(db.String(100), nullable=False)  # 名前
    overview = db.Column(db.String(200), nullable=False)  # 概要
    price = db.Column(db.Integer, nullable=False)  # 価格
    category = db.Column(db.String(100), nullable=False)  # カテゴリー
    image_path = db.Column(db.String(200), nullable=True)  # 画像パス

# カートモデル
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主キー
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # ユーザーID（外部キー）
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)  # アイテムID（外部キー）
    quantity = db.Column(db.Integer, nullable=False, default=1)  # 数量

    user = db.relationship('User', backref=db.backref('carts', lazy=True))  # ユーザーとのリレーションシップ
    item = db.relationship('Item', backref=db.backref('carts', lazy=True))  # アイテムとのリレーションシップ
