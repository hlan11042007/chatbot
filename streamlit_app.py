import streamlit as st
from openai import OpenAI

# === GIAO DIỆN ===
st.set_page_config(page_title="Chatbot Vật Lý", page_icon="⚡", layout="centered")

# CSS tùy chỉnh (phong cách trẻ trung, năng động)
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #e0f7fa, #fffde7);
            color: #222;
        }
        .stApp {
            background: linear-gradient(135deg, #c8e6c9, #fff9c4);
        }
        h1 {
            text-align: center;
            color: #2e7d32;
            font-family: 'Segoe UI', sans-serif;
        }
        .stChatInput input {
            border-radius: 12px;
            border: 1.5px solid #4caf50;
        }
    </style>
""", unsafe_allow_html=True)

# === TIÊU ĐỀ & GIỚI THIỆU ===
st.title("⚡ Chatbot Học Tập ⚡")
st.caption("Khám phá thế giới Vật Lý cùng trí tuệ nhân tạo – học hỏi, sáng tạo và phát triển!")

# === KẾT NỐI OPENAI ===
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# === LƯU LỊCH SỬ ===
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Bạn là Chatbot vui vẻ, nói tiếng Việt, chuyên giúp học sinh Việt Nam hiểu Vật Lý dễ hơn. Hãy truyền cảm hứng học tập!"}
    ]

# === HIỂN THỊ TIN NHẮN CŨ ===
for msg in st.session_state.messages[1:]:
    avatar = "👩‍🎓" if msg["role"] == "user" else "⚡"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# === NHẬP CÂU HỎI ===
if prompt := st.chat_input("Nhập câu hỏi Vật Lý của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👩‍🎓"):
        st.markdown(prompt)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            stream=True,
        )

        # Phản hồi trực tiếp
        with st.chat_message("assistant", avatar="⚡"):
            reply = st.write_stream(response)
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Lỗi: {e}")
