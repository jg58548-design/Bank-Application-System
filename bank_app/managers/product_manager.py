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


class ProductManager:
    """商品管理クラス"""

    def __init__(self):
        self.db = DatabaseManager()  # シングルトン活用

    @property  # 機能の後ろから括弧を省略させるデコレータ。デコレータはコードの前後に付けて使える機能。
    def all(self) -> pd.DataFrame:
        #全商品照会
        return self.db.query("SELECT * FROM products ORDER BY id")
        #productsの全内容をidを基準に並び替える。

    def __getitem__(self, product_id: int) -> pd.DataFrame:
        #pm[5]（idが5の部分）の形でアクセス可能 - マジックメソッド
        return self.db.query(
            "SELECT * FROM products WHERE id = ?",
            (product_id,)
        )

    def __len__(self) -> int:
         #len(pm)で商品数を確認
        return len(self.all)

    def search(self, keyword: str) -> pd.DataFrame:
        #キーワードで検索
        pattern = f'%{keyword}%'
        return self.db.query("""
            SELECT * FROM products 
            WHERE product_name LIKE ? OR product_description LIKE ?
            ORDER BY id
        """, (pattern, pattern))
        #SQL文法

    def filter(self, **kwargs) -> pd.DataFrame:
        #条件でフィルタリング。dfはユーザーが入力した値があるかどうかで、ないものを除外する。
        df = self.all
        for key, value in kwargs.items():
            if key in df.columns:
                df = df[df[key] == value]
        return df

    # 以前のメソッド
    def get_all_products(self):
        return self.all

    def search_products(self, keyword):
        return self.search(keyword)

    def get_product_by_id(self, product_id):
        return self[product_id]
