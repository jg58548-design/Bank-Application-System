# -*- coding: utf-8 -*-
import streamlit as st
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from managers.product_manager import ProductManager

st.set_page_config(
    page_title="商品申請窓口 - 金融商品を探す",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'is_logged_in' not in st.session_state or not st.session_state.get('is_logged_in', False):
    st.warning("️ ログインが必要なサービスです。")
    if st.button(" ログインへ", type="primary"):
        st.switch_page("pages/0_login.py")
    st.stop()

css_path = os.path.join(os.path.dirname(__file__), 'styles', 'main.css')
try:
    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

col_header1, col_header2, col_header3 = st.columns([6, 2, 2])

with col_header1: # ヘッダー 政府24参考
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

with col_header2:
    if st.button(" 申請履歴", use_container_width=True):
        st.switch_page("pages/3_my_applications.py")

with col_header3:
    st.markdown(f"""
    <div style="text-align: right; padding: 1rem 0;">
        <p style="font-size: 14px; color: #1e2124; margin: 0;">
             <strong>{st.session_state.get('customer_name', 'お客様')}様</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(" ログアウト", key="logout_btn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("ログアウトしました。")
        st.switch_page("pages/0_login.py")

st.markdown('<h1 style="font-size: 2rem; font-weight: 700; margin: 2rem 0 1rem 0; color: #1e2124;">金融商品を探す</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col1:
    search_query = st.text_input(
        "検索",
        placeholder="検索キーワードを入力してください（例：若者、積立、預金）",
        label_visibility="collapsed",
        key="search_input"
    )
with col2:
    search_button = st.button(" 検索", use_container_width=True)

#  Pythonicなクラスを使用
pm = ProductManager()

if search_button and search_query:
    products = pm.search(search_query)  # 簡潔なメソッド名
else:
    products = pm.all  # プロパティ使用

st.markdown(f'<p style="color: #666; font-size: 14px; margin: 1.5rem 0;">検索結果 <strong>{len(pm if not search_button else products)}件</strong></p>', unsafe_allow_html=True)

main_col, side_col = st.columns([7, 3])

with main_col:
    items_per_page = 8
    total_pages = (len(products) + items_per_page - 1) // items_per_page

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 1
        #初回アクセス時に商品ページを1に設定

    current_page = st.session_state['current_page']
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    current_products = products.iloc[start_idx:end_idx]

    if not current_products.empty:
        for _, product in current_products.iterrows():
            loan_limit = f"{int(product['product_loan_limit_amount']):,}万ウォン" if pd.notna(product['product_loan_limit_amount']) else "制限なし"

            st.markdown(f"""
            <div style="background: white; border: 1px solid #e1e4e7; border-radius: 12px; 
                        padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="flex: 1;">
                        <span style="background: #ecf2fe; color: #0b50d0; padding: 4px 12px; 
                                     border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block; margin-bottom: 0.5rem;">
                            金融商品
                        </span>
                        <h3 style="color: #1e2124 !important; font-size: 1.3rem; font-weight: 700; margin: 0.5rem 0;">
                            {product['product_name']}
                        </h3>
                        <p style="color: #464c53 !important; font-size: 0.95rem; line-height: 1.6; margin: 0.5rem 0 1rem 0;">
                            {product['product_description']}
                        </p>
                        <div style="display: flex; gap: 1.5rem; flex-wrap: wrap;">
                            <span style="color: #1e2124 !important; font-size: 0.9rem;">
                                <strong>金利：</strong>年 {product['product_interest_rate']}%
                            </span>
                            <span style="color: #1e2124 !important; font-size: 0.9rem;">
                                <strong>限度額：</strong>{loan_limit}
                            </span>
                            {'<span style="color: #1e2124 !important; font-size: 0.9rem;"><strong>年齢：</strong>' + str(int(product["product_min_age_requirement"])) + '〜' + str(int(product["product_max_age_requirement"])) + '歳</span>' if pd.notna(product.get('product_min_age_requirement')) and pd.notna(product.get('product_max_age_requirement')) else ''}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

            if st.button("申請する", key=f"btn_{product['id']}", type="primary", use_container_width=True):
                st.session_state['selected_product_id'] = int(product['id'])
                st.switch_page("pages/1_product_detail.py")

            st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        pagination_cols = st.columns([1, 1, 1, 1, 1, 1, 1])

        with pagination_cols[0]:
            if current_page > 1:
                if st.button("< 前へ", key="prev_page", use_container_width=True):
                    st.session_state['current_page'] -= 1
                    st.rerun()

        for i in range(total_pages):
            page_num = i + 1
            col_idx = i + 1
            if col_idx < len(pagination_cols):
                with pagination_cols[col_idx]:
                    if page_num == current_page:
                        st.markdown(f"""
                        <div style="background: #0b50d0; color: white; padding: 0.75rem; 
                                    text-align: center; border-radius: 8px; font-weight: 600;">
                            {page_num}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        if st.button(str(page_num), key=f"page_{page_num}", use_container_width=True):
                            st.session_state['current_page'] = page_num
                            st.rerun()
    else:
        st.info("検索結果がありません。")

with side_col:
    st.markdown("""
    <div class="sidebar-box">
        <h4 style="font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1e2124 !important;">
            最近見たサービス
        </h4>
        <p style="font-size: 14px; color: #666 !important;">
            まだ見たサービスはありません。
        </p>
    </div>

    <div class="sidebar-box">
        <h4 style="font-size: 16px; font-weight: 700; margin-bottom: 16px; color: #1e2124 !important;">
            直近1週間の人気サービス
        </h4>
        <ol style="padding-left: 20px; margin: 0;">
            <li style="font-size: 14px; margin-bottom: 8px; color: #333 !important;">若者優遇積立</li>
            <li style="font-size: 14px; margin-bottom: 8px; color: #333 !important;">シニア安心預金</li>
            <li style="font-size: 14px; margin-bottom: 8px; color: #333 !important;">会社員プラス口座</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
