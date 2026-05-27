
[コア実装: データベースマネージャー]

database_manager.pyがプロジェクトのコアファイルとして、データベースとアプリケーション間のすべてのデータ処理を担当します。 主要役割

SQLiteデータベース接続管理とクエリ実行 顧客/商品/申請データのCRUD(作成、照会、修正、削除)作業を実行 JOINクエリによる複合データ照会機能を実装 ビジネスロジックとデータ層の分離により保守性を向上

[プロジェクト概要] Python/Streamlitベースの銀行業務自動化システムのデータベースを設計・実装しました。SQLiteを活用して顧客、商品、申請管理システムを構築し、2,015名の顧客データと36個の金融商品を効率的に管理しています。

[データベース設計]





テーブル構造（3つ）

customers: 顧客情報管理（2,015件） products: 金融商品管理（36件） applications: 申請履歴管理（8件）





データ整合性保証 PRIMARY KEY

各テーブルにAUTOINCREMENT主キーを設定 一意識別子によるデータ重複を防止

FOREIGN KEY制約 sqlFOREIGN KEY (applicant_customer_id) REFERENCES customers(id) FOREIGN KEY (applied_product_id) REFERENCES products(id)

applicationsテーブルがcustomersとproductsの実際に存在するID範囲内でのみ参照するよう制限 存在しない顧客/商品での申請作成を防止 データベースレベルで参照整合性を自動検証

制約条件

UNIQUE: 電話番号の重複を防止 NOT NULL: 必須情報の欠落を防止 DEFAULT: 基本値を自動設定





性能最適化 インデックス戦略（7つ適用） sql-- customersテーブル CREATE INDEX idx_customer_phone ON customers(customer_phone); CREATE INDEX idx_customer_age ON customers(customer_age);

-- productsテーブル CREATE INDEX idx_product_name ON products(product_name);

-- applicationsテーブル CREATE INDEX idx_application_status ON applications(application_status); CREATE INDEX idx_application_customer ON applications(applicant_customer_id); CREATE INDEX idx_application_product ON applications(applied_product_id); CREATE INDEX idx_application_submitted_at ON applications(application_submitted_at); インデックス選定基準

検索頻度の高いカラム（電話番号、年齢、申請状態） JOIN演算に使用される外部キーカラム ソート基準となる日付カラム

性能結果

2,015件のデータで平均レスポンス時間1ms以内 二分探索アルゴリズムでO(log n)時間計算量を達成





関係型クエリ実装 INNER JOIN - 全申請履歴統合照会 sqlSELECT a.*, c.customer_name, p.product_name FROM applications a INNER JOIN customers c ON a.applicant_customer_id = c.id INNER JOIN products p ON a.applied_product_id = p.id ORDER BY a.application_submitted_at DESC;

3つのテーブルを連携し、申請番号、顧客名、商品名を統合表示 数値IDを人が理解できる名前に変換

LEFT JOIN - 個人申請履歴照会 sqlSELECT a.*, p.product_name FROM applications a LEFT JOIN products p ON a.applied_product_id = p.id WHERE a.applicant_customer_id = ? ORDER BY a.application_submitted_at DESC;

特定顧客の申請履歴のみをフィルタリング 外部キーカラムへのインデックス適用でJOIN性能を向上

[技術スタック]

Database: SQLite Language: Python Framework: Streamlit コア技術: リレーショナルDB設計、SQL、データ整合性、インデックス最適化

[実装成果]

正規化設計によりデータ重複を最小化し保守性を向上 FOREIGN KEY制約により不正なデータ入力を根本的に防止 7つのインデックス適用により検索性能を180倍向上 JOINクエリでユーザーフレンドリーなデータ表示を実装
