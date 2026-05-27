"""
コメント 宋正根 :) :D

 def __init__(self): これはProductManagerオブジェクトが生成される際に自身に与えるコマンドを記述したもの（defは定義）
 __init__は初期化（基本設定）関数
 __init__はコンピュータが実行時に最初に読み込み、最初に実行される基本関数と理解してよい
 クエリはデータベースから目的の値を取得するコマンド
 クエリはデータベースのコマンドなので文字列で記述する必要がある
 WHEREは特定条件の商品だけを取得するコマンド。?は空欄でinputのようなもの
 paramsは引数を受け取るコマンド
データベースのコードは文字列で書いてもquery =となっていれば読み込まれるので問題ない
データの流れ [UIリクエスト] -> [ProductManager関数呼び出し] -> [クエリ（命令書）作成] -> [DBからデータ取得（Fetch）] -> [UIへ結果返却]
"""
import pandas as pd
from config.database import DatabaseManager


class CustomerManager:
    """顧客管理クラス"""

    def __init__(self):
        self.db = DatabaseManager()   # シングルトン活用

    def __getitem__(self, customer_id: int) -> pd.DataFrame: #cm[1]の形でIDで照会
        return self.db.query(
            "SELECT * FROM customers WHERE id = ?",
            (customer_id,)
        )

    def find_by_phone(self, phone: str) -> pd.DataFrame: #電話番号で照会。初回ログイン時に使用。
        return self.db.query(
            "SELECT * FROM customers WHERE customer_phone = ?",
            (phone,)
        )

    def create(self, **kwargs) -> int: #顧客作成。辞書にまとめて後で取り出す。
        #kwargsはキーワード引数を意味する変数名で、**は値をまとめて後で取り出せる機能。現時点では空。
        return self.db.execute("""
            INSERT INTO customers 
            (customer_name, customer_phone, customer_age, customer_monthly_income,
             customer_credit_grade, customer_has_overdue, customer_existing_loan_count,
             customer_is_employed, customer_has_salary_transfer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            kwargs.get('name'),
            kwargs.get('phone'),
            kwargs.get('age'),
            kwargs.get('income'),
            kwargs.get('credit_grade'),
            kwargs.get('is_overdue', 0),
            0, 0, 0
        ))

    # 以前のメソッド
    def get_by_phone(self, phone):
        return self.find_by_phone(phone)

    def get_by_id(self, customer_id):
        return self[customer_id]
