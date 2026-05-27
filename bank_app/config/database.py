"""
コメント 宋正根
このdatabase.pyは結論として
アプリ内のデータをPythonコードから修正でき
ユーザーがアプリを起動したときに読み込むパスを設定し
エラーを防ぐ機能を追加したもの
"""

# -*- coding: utf-8 -*-
"""
上記はこのファイル内に韓国語コメントを書いてもコンピュータが文字化けせず正しく読めるよう、エンコード形式を指定するルール
実行フロー = スレッド
シングルトンの概念からまず理解する必要がある。プログラムを実行するとフローであるスレッドが生成されるが、
StreamlitのWebプログラミングは複数人が同時にアクセスするWebサイトのため、1人あたり複数のスレッドが生成される。
スレッドが重複してしまい、5人が利用している際に1人がローン申請をすると、金額が5倍にコピーされる可能性がある。また書き込みもできなくなる。
さらにサーバーを管理するメインコンピュータがダウンする可能性がある。
そのためシングルトン（どれだけフローが増えてもヒープへの接続通路は一つだけに固定して共有する）が必要。
SQLiteデータベースエンジン内部の自前のファイルロック（File Lock）メカニズムと
コードに記述されたトランザクション（commit/rollback）機能が動作しているため。
複数人が同時に修正すると値がバラバラになるので、更新を順番待ちさせて順序通りに処理し、
次の人には更新済みの値を確認させるためのもの。

ユーザーの命令を受けてインスタンスを取得しようとヒープ領域に向かう処理を、順番待ちにするのがシングルトンパターン。
通路が複数あるとメモリが溢れる。
"""
import sqlite3
import pandas as pd
from contextlib import contextmanager
"""元々Pythonのwith構文は自動でファイルを閉じるために作られたもの。
しかしsqlite3ではwithを使っても自動クローズが行われない。そのためcontextlibライブラリのこの機能を使う必要がある。
withを使って中のインデント内容が終わると自動で終了する機能。"""



class DatabaseManager: #シングルトンパターン DB接続管理クラス
    _instance = None # 最初にユーザーが起動したときに生成された最初のスレッドが通る場所。ここが通路になる。非常に重要！！！！！！！！！！！！！！！

    def __new__(cls, db_path='bank.db'):
        #__名前__はマジックメソッド（Magic Method）。ヒープにアクセスして新しいオブジェクトを「生成」する役割を専任する。メモリを操作できるメソッド。
        if cls._instance is None:
            """スタックにあるDatabaseManagerクラスのアドレスを通じて、スタティックにあるインスタンスのアドレスが存在しない場合、
            オブジェクトにコマンドを使ってヒープにインスタンスを作成し、
            そのアドレスをスタティック内のクラス領域に保存する。
            """
            cls._instance = super().__new__(cls) #superは上位の祖先をすべて探す関数。__new__というコマンドが元々存在していたが、強制的に使用する。
            cls._instance.db_path = db_path #db_pathにはbank.dbという情報だけを入れておく。
        return cls._instance #returnは処理を終えて戻るもの。終了の中括弧の最後と同じようなもの。

    @contextmanager #デコレータ。デコレータはコードの前後に付けて使える機能。
    def get_connection(self):

        conn = sqlite3.connect(self.db_path) #データベースのアドレス値を取得する。
        conn.execute("PRAGMA foreign_keys = ON")  # 接続ごとにFKを有効化
        try: # try - except エラーが発生しても強制終了せず、まず試してみるという意味。
            yield conn
            """
            tryと一緒に使うreturnのようなもの。
            yieldの意味は「一旦ここで止まって、後で呼ばれたら続きをやる」という意味。
            データベースから取得するデータが多すぎて一度に取得するとメモリが溢れそうなときに使用する。
            大量のデータを一件送って一時停止、また一件送って一時停止という形で処理する。動画のバッファリングと同じメカニズム。
            """
            conn.commit() #commit()はセーブと同じ。接続が正常だった内容を保存する。
        except Exception as e: #エラーが発生したら例外処理へ退避する。
            conn.rollback() #接続失敗時に元に戻す。
            raise e #エラー内容を投げる。
        finally: #最後に必ず実行する。
            conn.close() #データベースが壊れないよう接続を閉じる。

    def query(self, sql: str, params=None) -> pd.DataFrame: # pandas使用、参照用コード
        #クエリ：データベース内のデータにアクセスできるコード
        with self.get_connection() as conn:
            return pd.read_sql_query(sql, conn, params=params or ()) #データが空の場合は空を返す。
            #pd.read_sql_queryはデータベース（SQL）からデータを読み込む関数。

    def execute(self, sql: str, params=None) -> int: # 実行・削除・修正コード
        with self.get_connection() as conn:
            cursor = conn.cursor() # カーソルはデータを修正できるようにする関数。
            cursor.execute(sql, params or ())
            return cursor.lastrowid if sql.strip().upper().startswith('INSERT') else cursor.rowcount
        """「会員登録が完了しました（会員番号15番）」「修正されました（1件変更）」のようなメッセージを表示できるのは、
        execute関数がデータベースを実際に変更した後、その結果値（数値）を渡すため。"""
    # 以前のメソッドは後方互換性のために維持
    def fetch_data(self, query, params=None):
        #以前の関数をそのまま使うもの。queryと同じ。気にしなくてよい。
        return self.query(query, params)

    def execute_query(self, query, params=None):
        #以前の関数をそのまま使うもの。executeと同じ。気にしなくてよい。
        return self.execute(query, params)
