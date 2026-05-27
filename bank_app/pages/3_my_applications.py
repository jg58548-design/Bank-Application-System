# -*- coding: utf-8 -*-
"""
申請履歴（簡略バージョン）
"""
import streamlit as st
import os
from config.database import DatabaseManager
import pandas as pd
from datetime import datetime, timedelta

# ページ設定
st.set_page_config(
    page_title="申請履歴 - 商品申請窓口",
    page_icon="",
    layout="wide"
)

# CSSロード
css_path = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.css')
try:
    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# 簡略スタイルCSS
st.markdown("""
<style>
/* 検索エリア */
.search-box {
    background: #f8f9fa;
    padding: 1.5rem;
    margin: 2rem 0;
    border: 1px solid #dee2e6;
}

/* テーブルスタイル */
.gov-table {
    width: 100%;
    border-collapse: collapse;
    margin: 2rem 0;
    background: white;
}

.gov-table th {
    background: #1e3a8a;
    color: white;
    padding: 1rem;
    text-align: center;
    font-weight: 600;
    border: 1px solid #dee2e6;
}

.gov-table td {
    padding: 1rem;
    text-align: center;
    border: 1px solid #dee2e6;
    color: #212529;
}

.gov-table tr:hover {
    background: #f8f9fa;
}

/* ステータスバッジ */
.status-badge {
    display: inline-block;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.9rem;
}

.status-pending {
    background: #fff3cd;
    color: #856404;
}

.status-approved {
    background: #d1ecf1;
    color: #0c5460;
}

.status-complete {
    background: #d4edda;
    color: #155724;
}

.status-rejected {
    background: #f8d7da;
    color: #721c24;
}
</style>
""", unsafe_allow_html=True)

# ヘッダー
st.markdown("""
<div class="brand-container">
  <a href="/" class="brand-link">
    <div class="brand-icon-wrapper">
      <svg class="brand-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2"/>
        <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2"/>
        <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2"/>
      </svg>
    </div>
    <span class="brand-text">商品申請窓口</span>
  </a>
</div>
""", unsafe_allow_html=True)

# ログインチェック
if 'customer_id' not in st.session_state:
    st.warning("ログインが必要なサービスです。")
    if st.button("ログインへ", type="primary"):
        st.switch_page("pages/0_login.py")
    st.stop()

# タイトル
st.markdown("""
<h1 style="font-size: 1.8rem; font-weight: 700; margin: 2rem 0 1rem 0; border-bottom: 3px solid #1e3a8a; padding-bottom: 1rem;">
    サービス申請履歴
</h1>
""", unsafe_allow_html=True)

# オンライン申請商品タブ（単一）
st.markdown("""
<div style="background: #1e3a8a; color: white; padding: 1rem; text-align: center; font-weight: 600; font-size: 1rem;">
    オンライン申請商品
</div>
""", unsafe_allow_html=True)

# 案内メッセージ
st.markdown("""
<div style="background: #fff3cd; padding: 0.75rem 1rem; margin: 1rem 0; border-left: 4px solid #ffc107;">
    <span style="color: #856404;">※ 3日以前の申請内容は検索期間を入力してご確認ください。</span>
</div>
""", unsafe_allow_html=True)

# 検索エリア
st.markdown('<div class="search-box">', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("**期間別検索**")
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("開始日", datetime.now() - timedelta(days=30), label_visibility="collapsed", key="start")
    with date_col2:
        end_date = st.date_input("終了日", datetime.now(), label_visibility="collapsed", key="end")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("検索", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# DB照会
db = DatabaseManager()

query = """
    SELECT 
        a.id,
        a.application_number,
        a.application_submitted_at,
        a.application_status,
        c.customer_name,
        p.product_name
    FROM applications a
    LEFT JOIN customers c ON a.applicant_customer_id = c.id
    LEFT JOIN products p ON a.applied_product_id = p.id
    WHERE a.applicant_customer_id = ?
    ORDER BY a.application_submitted_at DESC
"""

df = db.query(query, (st.session_state['customer_id'],))

# テーブル表示
if not df.empty:
    st.markdown(f"""
    <div style="text-align: right; margin: 1rem 0; color: #666;">
        合計 <strong>{len(df)}</strong>件の申請履歴があります。
    </div>
    """, unsafe_allow_html=True)

    # データ行
    for idx, row in df.iterrows():
         #一度に全て取得せず、iterrows()でデータを1行ずつ取得して処理する
        # 日付フォーマット
        applied_date = pd.to_datetime(row['application_submitted_at']).strftime('%Y年%m月%d日')

        # ステータス別スタイル
        status_class = {
            '申請完了': 'status-complete',
            '審査中': 'status-pending',
            '承認': 'status-approved',
            '却下': 'status-rejected'
        }.get(row['application_status'], 'status-pending')

        # 処理状態テキスト
        status_text = {
            '申請完了': '処理完了（出力済み）',
            '審査中': '書類作成',
            '承認': '処理完了',
            '却下': '処理完了'
        }.get(row['application_status'], row['application_status'])

        # カード形式で表示
        st.markdown(f"""
        <div style="background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1rem; align-items: center;">
                <div>
                    <strong style="font-size: 1.1rem;">{row['application_number']}</strong><br>
                    <span style="color: #666; font-size: 0.9rem;">[{applied_date}] {row['customer_name']}</span>
                </div>
                <div>
                    <strong>{row['product_name']}</strong>
                </div>
                <div>
                    <span class="status-badge {status_class}">{status_text}</span>
                </div>
                <div style="text-align: right;">
        """, unsafe_allow_html=True)

        # Streamlitボタン
        if st.button("申請取消", key=f"cancel_{row['id']}", type="secondary"):
            db.execute("DELETE FROM applications WHERE id = ?", (row['id'],))
            st.success(f"申請番号 {row['application_number']} が取り消されました！")
            st.rerun()

        st.markdown("""
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ページネーション
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <span style="display: inline-block; padding: 0.5rem 1rem; background: #1e3a8a; color: white; border-radius: 4px; font-weight: 600;">1</span>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: #f8f9fa; border: 1px solid #dee2e6; margin: 2rem 0;">
        <h3 style="color: #6c757d;">申請履歴がありません</h3>
        <p style="color: #adb5bd;">商品を申請するとここに表示されます。</p>
    </div>
    """, unsafe_allow_html=True)

# ホームへボタン
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("ホームへ", use_container_width=False):
    st.switch_page("Home.py")
