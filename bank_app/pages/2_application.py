# -*- coding: utf-8 -*-
"""
信用ローン申請書ページ（安全バージョン）
"""
import streamlit as st
import streamlit.components.v1 as components
import os
from config.database import DatabaseManager
import pandas as pd
import datetime
import base64

# ページ設定
st.set_page_config(
    page_title="信用ローン申請書 - 商品申請窓口",
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

# 選択された商品確認
if 'selected_product_id' not in st.session_state:
    st.warning("商品を選択してください。")
    if st.button("商品一覧へ"):
        st.switch_page("Home.py")
    st.stop()

# 商品情報照会
db = DatabaseManager()

product_query = f"""
    SELECT id, product_name as name, product_interest_rate as interest_rate, product_loan_limit_amount as loan_limit
    FROM products
    WHERE id = {st.session_state['selected_product_id']}
"""
product_df = db.query(product_query)

if product_df.empty:
    st.error("商品情報が見つかりません。")
    st.stop()

product = product_df.iloc[0]

# 商品名からタイプを判定
product_name = product['name']
if 'カード' in product_name or '카드' in product_name:
    form_image = 'card_application_form.png'
    form_title = 'カード発行申請書'
elif '예금' in product_name:
    form_image = 'deposit_application_form.png'
    form_title = '預金口座申請書'
elif '대출' in product_name:
    form_image = 'application_form.png'
    form_title = '信用ローン申請書'
elif '적금' in product_name:
    form_image = 'application_form.png'
    form_title = '積立申請書'
elif '통장' in product_name:
    form_image = 'application_form.png'
    form_title = '口座申請書'
else:
    form_image = 'application_form.png'
    form_title = '申請書'

# タイトル
st.markdown(f"<h1 style='text-align: center; font-size: 2rem; font-weight: 700; margin: 2rem 0;'>{form_title}</h1>", unsafe_allow_html=True)

# 画像をbase64にエンコード
image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', form_image)

if os.path.exists(image_path):
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode()

    # 高速Canvas
    canvas_html = f"""
    <div style="text-align: center; margin: 2rem auto; max-width: 900px;">
        <div style="position: relative; display: inline-block;">
            <canvas id="bgCanvas" style="position: absolute; top: 0; left: 0; border: 2px solid #333;"></canvas>
            <canvas id="drawCanvas" style="position: relative; cursor: crosshair; border: 2px solid #333;"></canvas>
        </div>
        <div style="margin-top: 1rem;">
            <button onclick="clearCanvas()" 
                    style="padding: 0.75rem 2rem; background: #dc3545; color: white; 
                           border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; 
                           font-weight: 600; margin-right: 1rem;">
                全て消す
            </button>
            <button onclick="undoLast()" 
                    style="padding: 0.75rem 2rem; background: #6c757d; color: white; 
                           border: none; border-radius: 8px; cursor: pointer; font-size: 1rem; 
                           font-weight: 600;">
                元に戻す
            </button>
        </div>
        <p style="color: #666; font-size: 0.9rem; margin-top: 1rem;">
             マウスやタッチで申請書に直接チェックや記入をしてください
        </p>
    </div>

    <script>
    const bgCanvas = document.getElementById('bgCanvas');
    const drawCanvas = document.getElementById('drawCanvas');
    const bgCtx = bgCanvas.getContext('2d');
    const drawCtx = drawCanvas.getContext('2d');

    const img = new Image();
    img.src = 'data:image/png;base64,{image_data}';

    let isDrawing = false;
    let strokes = [];

    drawCtx.strokeStyle = '#0000ff';
    drawCtx.lineWidth = 3;
    drawCtx.lineCap = 'round';
    drawCtx.lineJoin = 'round';

    img.onload = function() {{
        bgCanvas.width = drawCanvas.width = img.width;
        bgCanvas.height = drawCanvas.height = img.height;
        bgCtx.drawImage(img, 0, 0);
    }};

    function getCoords(canvas, e) {{
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {{
            x: (e.clientX - rect.left) * scaleX,
            y: (e.clientY - rect.top) * scaleY
        }};
    }}

    function getTouchCoords(canvas, e) {{
        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const touch = e.touches[0];
        return {{
            x: (touch.clientX - rect.left) * scaleX,
            y: (touch.clientY - rect.top) * scaleY
        }};
    }}

    drawCanvas.addEventListener('mousedown', (e) => {{
        isDrawing = true;
        const coords = getCoords(drawCanvas, e);
        drawCtx.beginPath();
        drawCtx.moveTo(coords.x, coords.y);
        strokes.push([{{x: coords.x, y: coords.y}}]);
    }});

    drawCanvas.addEventListener('mousemove', (e) => {{
        if (!isDrawing) return;
        const coords = getCoords(drawCanvas, e);
        drawCtx.lineTo(coords.x, coords.y);
        drawCtx.stroke();
        strokes[strokes.length - 1].push({{x: coords.x, y: coords.y}});
    }});

    drawCanvas.addEventListener('mouseup', () => {{
        isDrawing = false;
    }});

    drawCanvas.addEventListener('mouseout', () => {{
        isDrawing = false;
    }});

    drawCanvas.addEventListener('touchstart', (e) => {{
        e.preventDefault();
        isDrawing = true;
        const coords = getTouchCoords(drawCanvas, e);
        drawCtx.beginPath();
        drawCtx.moveTo(coords.x, coords.y);
        strokes.push([{{x: coords.x, y: coords.y}}]);
    }});

    drawCanvas.addEventListener('touchmove', (e) => {{
        e.preventDefault();
        if (!isDrawing) return;
        const coords = getTouchCoords(drawCanvas, e);
        drawCtx.lineTo(coords.x, coords.y);
        drawCtx.stroke();
        strokes[strokes.length - 1].push({{x: coords.x, y: coords.y}});
    }});

    drawCanvas.addEventListener('touchend', (e) => {{
        e.preventDefault();
        isDrawing = false;
    }});

    function redrawAll() {{
        drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
        strokes.forEach(stroke => {{
            if (stroke.length > 1) {{
                drawCtx.beginPath();
                drawCtx.moveTo(stroke[0].x, stroke[0].y);
                for (let i = 1; i < stroke.length; i++) {{
                    drawCtx.lineTo(stroke[i].x, stroke[i].y);
                }}
                drawCtx.stroke();
            }}
        }});
    }}

    function clearCanvas() {{
        strokes = [];
        drawCtx.clearRect(0, 0, drawCanvas.width, drawCanvas.height);
    }}

    function undoLast() {{
        if (strokes.length > 0) {{
            strokes.pop();
            redrawAll();
        }}
    }}
    </script>
    """

    components.html(canvas_html, height=1400)

else:
    st.error("申請書フォームの画像が見つかりません。")

# 完了ボタン
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("ホームへ", use_container_width=True):
        st.switch_page("Home.py")

with col3:
    if st.button("申請完了", type="primary", use_container_width=True):
        try:
            db = DatabaseManager()

            application_number = f"APP{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"

            # execute()使用
            db.execute("""
                INSERT INTO applications 
                (applicant_customer_id, applied_product_id, application_number, application_status, application_signature_image_data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                st.session_state['customer_id'],
                st.session_state['selected_product_id'],
                application_number,
                '申請完了',
                ''
            ))

            st.markdown(f"""
            <div style="background: #d4edda; border: 1px solid #c3e6cb; border-radius: 8px; 
                        padding: 1.5rem; margin: 2rem 0; text-align: center;">
                <h3 style="color: #155724; font-size: 1.5rem; font-weight: 700; margin: 0;">
                     申請が完了しました！
                </h3>
                <p style="color: #155724; font-size: 1.1rem; margin: 1rem 0 0 0;">
                    申請番号：{application_number}
                </p>
            </div>
            """, unsafe_allow_html=True)

            import time
            time.sleep(2)
            st.switch_page("pages/3_my_applications.py")

        except Exception as e:
            st.error(f"申請中にエラーが発生しました：{str(e)}")
