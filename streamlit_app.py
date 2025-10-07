import streamlit as st
from openai import OpenAI

# === CẤU HÌNH GIAO DIỆN ===
st.set_page_config(page_title="Chatbot Vật Lý", page_icon="⚡", layout="centered")

# CSS phong cách năng động, thân thiện với học sinh
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #d1f4ff, #fff9c4);
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            text-align: center;
            color: #0d47a1;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #1565c0;
            margin-bottom: 20px;
        }
        .author {
            text-align: center;
            font-size: 15px;
            color: #555;
            margin-top: 10px;
            font-style: italic;
        }
        .stChatInput input {
            border-radius: 10px;
            border: 1.5px solid #42a5f5;
        }
        .stMarkdown {
            font-size: 16px;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)

# === TIÊU ĐỀ & MÔ TẢ ===
st.title("⚡ Chatbot Vật Lý ⚡")
st.markdown('<p class="subtitle">Khám phá Vật Lý dễ hiểu cùng trí tuệ nhân tạo – học nhanh, hiểu sâu, sáng tạo không giới hạn! 🇻🇳</p>', unsafe_allow_html=True)
st.markdown('<p class="author">Tác giả: <b>Hoàng Lân</b></p>', unsafe_allow_html=True)

# === KẾT NỐI OPENAI ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === LƯU LỊCH SỬ HỘI THOẠI ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Bạn là Chatbot nói tiếng Việt, thân thiện và chuyên giải thích Vật Lý dễ hiểu cho học sinh Việt Nam."}
    ]

# === HIỂN THỊ TIN NHẮN TRƯỚC ===
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Ô NHẬP TIN NHẮN ===
if prompt := st.chat_input("Nhập câu hỏi hoặc chủ đề Vật Lý bạn muốn học..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        # Ghi phản hồi ra giao diện
        with st.chat_message("assistant"):
            reply = st.write_stream(response)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Lỗi: {e}")
