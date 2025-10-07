import streamlit as st
from openai import OpenAI
import os

# === CẤU HÌNH TRANG ===
st.set_page_config(page_title="Chatbot Vật Lý", page_icon="⚡", layout="centered")

# === CSS DARK MODE + ẢNH TRÒN ===
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0a0f1f, #1a1a40);
            color: #e0e0e0;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            text-align: center;
            color: #82b1ff;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #90caf9;
            margin-bottom: 10px;
        }
        .author {
            text-align: center;
            font-size: 15px;
            color: #aaa;
            margin-top: -5px;
            font-style: italic;
        }
        .stChatInput input {
            border-radius: 10px;
            border: 1.5px solid #42a5f5;
            background-color: #121212;
            color: white;
        }
        .stMarkdown {
            font-size: 16px;
            line-height: 1.6;
        }
        img.banner {
            display: block;
            margin-left: auto;
            margin-right: auto;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(66,165,245,0.5);
            margin-bottom: 20px;
        }
        img.avatar {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 160px;
            height: 160px;
            border-radius: 50%;
            object-fit: cover;
            box-shadow: 0 0 15px rgba(66,165,245,0.5);
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# === ẢNH AVATAR TÁC GIẢ ===
author_image_path = "hoanglan.jpg"
if os.path.exists(author_image_path):
    st.markdown(f'<img src="{author_image_path}" class="avatar">', unsafe_allow_html=True)
else:
    st.warning("⚠️ Chưa tìm thấy ảnh 'hoanglan.jpg' trong thư mục dự án.")

# === TIÊU ĐỀ & MÔ TẢ ===
st.title("⚡ Chatbot Vật Lý ⚡")
st.markdown('<p class="subtitle">Khám phá Vật Lý cùng trí tuệ nhân tạo – học nhanh, hiểu sâu, sáng tạo không giới hạn!</p>', unsafe_allow_html=True)
st.markdown('<p class="author">Tác giả: <b>Hoàng Lân</b></p>', unsafe_allow_html=True)

# === KẾT NỐI OPENAI ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === LỊCH SỬ CHAT ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Bạn là Chatbot nói tiếng Việt, thân thiện và chuyên giải thích Vật Lý dễ hiểu cho học sinh Việt Nam."}
    ]

# === HIỂN THỊ LỊCH SỬ ===
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Ô NHẬP CHAT ===
if prompt := st.chat_input("Nhập câu hỏi hoặc chủ đề bạn muốn hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        # Hiển thị phản hồi
        with st.chat_message("assistant"):
            reply = st.write_stream(response)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Lỗi: {e}")
