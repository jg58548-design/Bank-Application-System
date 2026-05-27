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
import datetime
from config.database import DatabaseManager


class ApplicationManager: #申請管理クラス

    def __init__(self):
        #Pythonでオブジェクト（インスタンス）が生成された直後、
        # オブジェクト内部の変数（データ）を初めて設定する際に自動的に呼び出される「初期化マジックメソッド」
        self.db = DatabaseManager()  # シングルトン活用。DatabaseManagerクラスの機能を呼び出す。

    def __getitem__(self, app_id: int) -> pd.DataFrame:
        #データベースからデータをID番号で取得する。am[1]の形でIDで照会
        return self.db.query(
            "SELECT * FROM applications WHERE id = ?",
            (app_id,)
        )
        #WHEREは条件に合うものだけを抽出する。SELECTはその行をコピーするという意味。

    def by_customer(self, customer_id: int) -> pd.DataFrame: #顧客別申請履歴
        return self.db.query("""
            SELECT 
                a.id, a.application_number, a.application_status, 
                a.application_submitted_at, p.product_name
            FROM applications a
            LEFT JOIN products p ON a.applied_product_id = p.id
            WHERE a.applicant_customer_id = ?
            ORDER BY a.application_submitted_at DESC
        """, (customer_id,))
         #顧客の申請履歴を取得。左側は全件、右側は左側との共通部分のみ。

    def create(self, customer_id: int, product_id: int, **kwargs) -> tuple:
       # 申請内容をアプリケーションデータベースに保存する機能
        #**kwargsはキーワード引数を意味する変数名で、**は値をまとめて後で取り出せる機能。現時点では空。

        app_number = f"APP{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
        # 申請時の現在日時を記録する。strftimeはフォーマットで時間を表示し、前の部分は現在時刻を取得する。
        app_id = self.db.execute("""
            INSERT INTO applications 
            (applicant_customer_id, applied_product_id, application_number,
             application_status, application_signature_image_data, 
             application_documents_submitted)
            VALUES (?, ?, ?, '申請完了', ?, 0)
        """, (
            customer_id, product_id, app_number,
            kwargs.get('signature', '')
        ))

        return app_id, app_number
        #署名機能は未実装。今後実装予定。

    def delete(self, app_id: int) -> bool: #申請削除機能
        """申請削除 - bool返却"""
        rows = self.db.execute(
            "DELETE FROM applications WHERE id = ?",
            (app_id,)
        )
        return rows > 0

    def get_by_customer(self, customer_id): # 以前のメソッド互換用
        return self.by_customer(customer_id)

    def create_application(self, customer_id, product_id, signature=''): # 以前のメソッド互換用
        return self.create(customer_id, product_id, signature=signature)
