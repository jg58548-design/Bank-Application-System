# -*- coding: utf-8 -*-
"""
商品詳細ページ（政府24スタイル + 資格確認）
"""
import streamlit as st
import pandas as pd
import os
from config.database import DatabaseManager

# ページ設定
st.set_page_config(
    #layoutは画面の横幅を調整するもの。広く使うために設定。
    page_title="商品詳細 - 商品申請窓口",
    page_icon="",
    layout="wide"
)

# CSSロード
css_path = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.css')
# 詳細ページの位置がpagesフォルダ内のため親フォルダが見つからないので、
# osナビゲーションを使って絶対パスを調べた後、
# os.path.abspath(__file__) = C:\Python練習スペース\bank_app_pythonic\pages\1_product_detail.py
# 末尾から一つ上に移動し
# os.path.dirname() = C:\Python練習スペース\bank_app_pythonic\pages
# replace('/pages', '') = pagesフォルダを切り取り
# sys.path.append(...) = 基本アドレスリストに追加
# 以降クラスのインポートが可能
try:
    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

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

# 選択された商品IDの確認
if 'selected_product_id' not in st.session_state:
    st.warning("商品を選択してください。")
    if st.button(" 商品一覧に戻る"):
        st.switch_page("Home.py")
    st.stop()
    """
    前のページ（ホーム）で商品をクリックして次のページ（詳細）に移動すると、
    Webサイトはどの商品を選択したか忘れてしまう。
    そのため商品をクリックするとその商品IDがセッションに保存され、
    もし商品ページに商品セッションがなければホームに戻る。
    """

# 商品情報照会
db = DatabaseManager() # ilocのために必要

query = f"""
    SELECT id, product_name, product_description, product_interest_rate, product_loan_limit_amount, 
           product_min_age_requirement, product_max_age_requirement, product_min_income_requirement, product_min_income_requirement as min_annual_income, 
           product_min_credit_score_requirement, product_max_dti_ratio, product_required_documents,
           'category' as category, 'product_type' as product_type, product_requires_manual_review
    FROM products
    WHERE id = {st.session_state['selected_product_id']}
"""

product_df = db.query(query)  #  DatabaseManagerのquery()使用

if product_df.empty:
    st.error("商品情報が見つかりません。")
    st.stop()

product = product_df.iloc[0]


# 上部バッジ
st.markdown(f"""
<div style="margin: 2rem 0 1rem 0;">
    <span style="background: #ecf2fe; color: #0b50d0; padding: 6px 14px; 
                 border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block;">
        金融商品
    </span>
</div>
""", unsafe_allow_html=True)
#unsafe_allow_html=True これが非常に重要。これがないとHTMLコードがそのまま表示されてしまう。

# 商品名ヘッダー 政府24風のコード
st.markdown(f"""
<h1 style="font-size: 2rem; font-weight: 700; color: #1e2124 !important; margin: 1rem 0;">
    {product['product_name']}
</h1>
""", unsafe_allow_html=True)

# 商品説明
st.markdown(f"""
<p style="font-size: 1.1rem; color: #464c53 !important; line-height: 1.7; margin: 1rem 0 2rem 0;">
    {product['product_description']}
</p>
""", unsafe_allow_html=True)

# 区切り線
st.markdown("<hr style='border: none; border-top: 1px solid #e1e4e7; margin: 2rem 0;'>", unsafe_allow_html=True)

# 申請方法
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    申請方法
</h3>
<p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
    窓口、郵便、電話、FAX、民願郵便、インターネット、モバイル
</p>
""", unsafe_allow_html=True)

# 申請資格
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    申請資格
</h3>
""", unsafe_allow_html=True)

# 資格条件
eligibility_text = []
if pd.notna(product.get('min_age')) and pd.notna(product.get('max_age')):
    if int(product['product_max_age_requirement']) == 100:
        eligibility_text.append(f"満{int(product['product_min_age_requirement'])}歳以上")
    else:
        eligibility_text.append(f"満{int(product['product_min_age_requirement'])}〜{int(product['product_max_age_requirement'])}歳")

if pd.notna(product.get('product_min_income_requirement')) and product['product_min_income_requirement'] > 0:
    eligibility_text.append(f"月収{int(product['product_min_income_requirement'])}万ウォン以上")

if pd.notna(product.get('product_min_income_requirement')) and product['product_min_income_requirement'] > 0:
    eligibility_text.append(f"年収{int(product['product_min_income_requirement'])}万ウォン以上")

if pd.notna(product.get('product_min_credit_score_requirement')) and product['product_min_credit_score_requirement'] > 0:
    eligibility_text.append(f"信用スコア{int(product['product_min_credit_score_requirement'])}点以上")

if pd.notna(product.get('product_max_dti_ratio')) and product['product_max_dti_ratio'] < 100:
    eligibility_text.append(f"DTI{product['product_max_dti_ratio']}%以下")

if eligibility_text:
    st.markdown(f"""
    <p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
        {', '.join(eligibility_text)}
    </p>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
        どなたでも申請可能
    </p>
    """, unsafe_allow_html=True)

# サービス内容
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    サービス内容
</h3>
""", unsafe_allow_html=True)

# 金利および限度額情報
if pd.notna(product.get('interest_rate')):
    rate_text = f"金利：年{product['product_interest_rate']}%"
else:
    rate_text = ""

if pd.notna(product.get('loan_limit')):
    if product['product_loan_limit_amount'] > 0:
        limit_text = f"限度額：最大{int(product['product_loan_limit_amount']):,}万ウォン"
    else:
        limit_text = "限度額：制限なし"
else:
    limit_text = ""

service_content = []
if rate_text:
    service_content.append(rate_text)
if limit_text:
    service_content.append(limit_text)

if service_content:
    st.markdown(f"""
    <p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
        {' / '.join(service_content)}
    </p>
    """, unsafe_allow_html=True)

# 処理期間
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    処理期間
</h3>
""", unsafe_allow_html=True)

if product.get('requires_manual_review') == 1:
    processing_time = "営業日基準2〜7日（行員による書類確認が必要）"
else:
    processing_time = "即時（営業時間内3時間）"

st.markdown(f"""
<p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
    {processing_time}
</p>
<p style="font-size: 0.9rem; color: #666 !important; margin-top: 0.5rem;">
    処理期間の計算方法 
</p>
""", unsafe_allow_html=True)

# 申請書
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    申請書
</h3>
""", unsafe_allow_html=True)

if pd.notna(product.get('required_docs')):
    docs = product['product_required_documents']
else:
    docs = "身分証明書"

st.markdown(f"""
<p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
    {docs}
</p>
<p style="font-size: 0.9rem; color: #666 !important; margin-top: 0.5rem;">
    申請記載例 
</p>
""", unsafe_allow_html=True)

# 手数料
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
    手数料
</h3>
<p style="font-size: 1rem; color: #464c53 !important; line-height: 1.7;">
    1筆地あたりインターネット発行・閲覧無料、窓口発行（1筆地）：500ウォン、窓口閲覧（1筆地）：300ウォン
</p>
""", unsafe_allow_html=True)

# 区切り線
st.markdown("<hr style='border: none; border-top: 1px solid #e1e4e7; margin: 3rem 0 2rem 0;'>", unsafe_allow_html=True)

# ===== 申請資格確認 =====
st.markdown("""
<h3 style="font-size: 1.3rem; font-weight: 700; color: #1e2124 !important; margin: 2rem 0 1rem 0;">
     申請資格確認
</h3>
""", unsafe_allow_html=True)

# ログインチェック
if 'customer_id' in st.session_state:
    # 顧客情報照会
    customer_query = f"""
        SELECT id, customer_name as name, customer_age as age, customer_monthly_income as income, 
               customer_monthly_income as monthly_income, 
               (customer_monthly_income * 12) as annual_income, 
               customer_credit_grade as credit_score,
               customer_credit_grade as credit_grade,
               customer_has_overdue as is_overdue,
               40 as dti
        FROM customers
        WHERE id = {st.session_state['customer_id']}
    """
    customer_df = db.query(customer_query)  #  db.query()使用

    if not customer_df.empty:
        customer = customer_df.iloc[0]

        # 資格検証
        is_eligible = True
        rejection_reasons = []

        # 年齢確認
        if pd.notna(product.get('min_age')) and pd.notna(product.get('max_age')):
            if customer['customer_age'] < product['product_min_age_requirement'] or customer['customer_age'] > product['product_max_age_requirement']:
                is_eligible = False
                rejection_reasons.append(f"年齢条件未達（要件：{int(product['product_min_age_requirement'])}〜{int(product['product_max_age_requirement'])}歳、現在：{customer['customer_age']}歳）")

        # 月収確認
        if pd.notna(product.get('product_min_income_requirement')) and product['product_min_income_requirement'] > 0:
            if customer['monthly_income'] < product['product_min_income_requirement']:
                is_eligible = False
                rejection_reasons.append(f"月収条件未達（要件：{int(product['product_min_income_requirement'])}万ウォン以上、現在：{int(customer['monthly_income'])}万ウォン）")

        # 年収確認
        if pd.notna(product.get('product_min_income_requirement')) and product['product_min_income_requirement'] > 0:
            if customer['annual_income'] < product['product_min_income_requirement']:
                is_eligible = False
                rejection_reasons.append(f"年収条件未達（要件：{int(product['product_min_income_requirement'])}万ウォン以上、現在：{int(customer['annual_income'])}万ウォン）")

        # 信用スコア確認
        if pd.notna(product.get('product_min_credit_score_requirement')) and product['product_min_credit_score_requirement'] > 0:
            if customer['credit_score'] < product['product_min_credit_score_requirement']:
                is_eligible = False
                rejection_reasons.append(f"信用スコア条件未達（要件：{int(product['product_min_credit_score_requirement'])}点以上、現在：{customer['credit_score']}点）")

        # DTI確認
        if pd.notna(product.get('product_max_dti_ratio')) and product['product_max_dti_ratio'] < 100:
            if customer['dti'] > product['product_max_dti_ratio']:
                is_eligible = False
                rejection_reasons.append(f"DTI条件未達（要件：{product['product_max_dti_ratio']}%以下、現在：{customer['dti']}%）")

        # 結果表示
        if is_eligible:
            st.markdown("""
            <div style="background: #d1f2eb; border: 2px solid #1abc9c; border-radius: 12px; 
                        padding: 2rem; margin: 1rem 0;">
                <h4 style="color: #0e6655; font-size: 1.3rem; font-weight: 700; margin: 0 0 0.5rem 0;">
                     申請可能です
                </h4>
                <p style="color: #0e6655; font-size: 1rem; margin: 0;">
                    すべての申請資格を満たしています！
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # 不可理由表示
            reasons_html = "<br>".join([f"• {reason}" for reason in rejection_reasons])
            st.markdown(f"""
            <div style="background: #ffe5e5; border: 2px solid #e74c3c; border-radius: 12px; 
                        padding: 2rem; margin: 1rem 0;">
                <h4 style="color: #c0392b; font-size: 1.3rem; font-weight: 700; margin: 0 0 1rem 0;">
                     申請不可です
                </h4>
                <div style="color: #c0392b; font-size: 1rem; line-height: 1.8;">
                    {reasons_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("顧客情報が見つかりません。")
else:
    st.info("ログインすると申請資格を確認できます。")

# 下部ボタン
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("商品一覧へ", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    # ログインチェックおよび資格確認
    if 'customer_id' not in st.session_state:
        if st.button(" ログインして申請する", type="primary", use_container_width=True):
            st.switch_page("pages/0_login.py")
    elif is_eligible:
        if st.button(" 申請する", type="primary", use_container_width=True):
            st.session_state['selected_product_id'] = int(product['id'])
            st.switch_page("pages/2_application.py")
    else:
        st.button(" 申請不可", type="primary", use_container_width=True, disabled=True)
