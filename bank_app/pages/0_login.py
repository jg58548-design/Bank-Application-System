# -*- coding: utf-8 -*-
# SMS認証実装
# 現在は電話番号のみ入力
import streamlit as st
from managers.customer_manager import CustomerManager
import random
import os

# 電話番号正規化関数
def normalize_phone(phone): #電話番号からハイフンを除去
    return phone.replace('-', '').replace(' ', '')

def format_phone(phone): #電話番号を010-1234-5678形式に変換
    phone = normalize_phone(phone)
    if len(phone) == 11:
        return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
    return phone

# ページ設定
st.set_page_config(
    page_title="ログイン",
    page_icon="",
    layout="wide"
)

# CSSロード
css_path = os.path.join(os.path.dirname(__file__), '..', 'styles', 'main.css')
try:
    with open(css_path, encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSSファイルが見つかりません。")

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

# ページタイトル
st.markdown("""
<div style="margin: 2rem 0; text-align: center;">
    <h1 style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e2124;">
        ログイン
    </h1>
    <p style="font-size: 1rem; color: #464c53;">
        携帯電話番号で簡単にログインできます
    </p>
</div>
""", unsafe_allow_html=True)

# ログインフォーム（中央寄せ）
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="background: white; border: 1px solid #e1e4e7; border-radius: 12px; 
                padding: 2rem; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);">
    """, unsafe_allow_html=True)

    # セッション状態初期化
    if 'auth_step' not in st.session_state:
        st.session_state['auth_step'] = 'phone'  # phone, verify
    if 'auth_code' not in st.session_state:
        st.session_state['auth_code'] = None
    if 'phone_number' not in st.session_state:
        st.session_state['phone_number'] = None

    # Step 1: 携帯電話番号入力
    if st.session_state['auth_step'] == 'phone':
        st.markdown("### 携帯電話番号入力")

        phone = st.text_input(
            "携帯電話番号",
            placeholder="010-1234-5678",
            #placeholder ここにどのような形式で入力するかを案内する表示
            help="'-'を含めて入力してください",
            key="phone_input"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("認証番号を受け取る", type="primary", use_container_width=True): # ボタンがログイン、デフォルトスキン
            if not phone:
                st.error("携帯電話番号を入力してください。")
            elif len(normalize_phone(phone)) != 11:
                st.error("正しい携帯電話番号の形式ではありません。")
            else:
                # 認証番号生成（6桁）
                auth_code = str(random.randint(100000, 999999))
                st.session_state['auth_code'] = auth_code
                st.session_state['phone_number'] = format_phone(phone)
                st.session_state['auth_step'] = 'verify'
                st.rerun()

    # Step 2: 認証番号確認
    elif st.session_state['auth_step'] == 'verify':
        st.markdown(f"### {st.session_state['phone_number']}")

        # デモ用：認証番号表示
        st.info(f"""
        **[デモ用認証番号]** `{st.session_state['auth_code']}`

        *実際のサービスではSMSで送信されます。*
        """)

        input_code = st.text_input(
            "認証番号入力",
            placeholder="6桁の数字",
            max_chars=6,
            key="code_input"
        )

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("番号変更", use_container_width=True):
                st.session_state['auth_step'] = 'phone'
                st.session_state['auth_code'] = None
                st.session_state['phone_number'] = None
                st.rerun()

        with col_b:
            if st.button("ログイン", type="primary", use_container_width=True):
                if not input_code:
                    st.error("認証番号を入力してください。")
                elif input_code != st.session_state['auth_code']:
                    st.error("認証番号が一致しません。")
                else:
                    # ログイン成功
                    customer_manager = CustomerManager()
                    customer = customer_manager.get_by_phone(st.session_state['phone_number'])

                    if not customer.empty:
                        #新規顧客登録ページへの遷移（会員登録するかどうか検討中）
                        st.session_state['customer_id'] = int(customer.iloc[0]['id'])
                        st.session_state['customer_name'] = customer.iloc[0]['customer_name'] #ilocはpandasの機能で0番目の内容（顧客IDのある行）をすべて取得する
                        st.session_state['customer_phone'] = customer.iloc[0]['customer_phone'] #ilocはpandasの機能で0番目の内容（顧客IDのある行）をすべて取得する

                        st.session_state['is_logged_in'] = True

                        # 初期化
                        st.session_state['auth_step'] = 'phone'
                        st.session_state['auth_code'] = None
                        st.session_state['phone_number'] = None

                        # ホームへ移動
                        st.markdown("しばらくすると自動的に移動します...")
                        import time
                        time.sleep(2)
                        st.switch_page("Home.py")
                    else:
                        # 新規顧客 - 会員登録が必要
                        st.warning("""
                        **登録されていない番号です。**

                        会員登録が必要です。申請ページで情報を入力してください。
                        """)

                        # 一時セッション保存（会員登録用）
                        st.session_state['temp_phone'] = st.session_state['phone_number']

                        if st.button("会員登録へ"):
                            st.switch_page("pages/2_application.py")

    st.markdown("</div>", unsafe_allow_html=True)

# 案内事項
st.markdown("---")

# 開発者モード（ログインスキップ）
st.markdown("""
<div style="background: #f0f0f0; border: 2px dashed #999; border-radius: 12px; 
            padding: 1.5rem; text-align: center;">
    <h4 style="color: #666; font-size: 1rem; margin-bottom: 0.5rem;">
        開発者モード
    </h4>
    <p style="color: #888; font-size: 0.9rem; margin: 0;">
        テスト用 - ログインなしで直接アクセス
    </p>
</div>
""", unsafe_allow_html=True)

col_dev1, col_dev2, col_dev3 = st.columns([1, 2, 1])
with col_dev2:
    if st.button("ログインスキップ（開発者モード）", use_container_width=True):
        # 一時セッション作成
        st.session_state['customer_id'] = 1
        st.session_state['customer_name'] = "テストユーザー"
        st.session_state['customer_phone'] = "010-1234-5678"
        st.session_state['is_logged_in'] = True

        import time
        time.sleep(1)
        st.switch_page("Home.py")

st.markdown("---")

st.info("""
### ご案内
- このシステムは**デモ用**です。実際のSMSは送信されません。
- 認証番号は画面に表示されます。
- 登録済みの顧客のみログインできます。
""")
