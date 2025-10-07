import streamlit as st
from openai import OpenAI

# 🌙 Giao diện dark mode + CSS trang trí
st.markdown("""
    <style>
        body {
            background-color: #0f0f0f;
            color: #f5f5f5;
        }
        .banner {
            width: 100%;
            border-radius: 14px;
            margin-bottom: 20px;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.25);
            animation: pulse 4s infinite ease-in-out;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 20px rgba(0,255,255,0.2); }
            50% { box-shadow: 0 0 40px rgba(0,255,255,0.5); }
            100% { box-shadow: 0 0 20px rgba(0,255,255,0.2); }
        }
        .avatar {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 90px;
            height: 90px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid #00ffff80;
            box-shadow: 0 0 15px rgba(0,255,255,0.4);
        }
        .footer {
            text-align: center;
            font-size: 15px;
            color: #aaa;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# 🧠 Banner minh hoạ vật lý (link ổn định từ Unsplash)
st.image(
    "https://images.unsplash.com/photo-1618886614638-1a6a2e1f9b40?auto=format&fit=crop&w=1400&q=80",
    use_container_width=True,
    caption="Khám phá tri thức Vật Lý cùng AI 🇻🇳",
)

# 🧩 Tiêu đề & mô tả
st.title("💬 Chatbot Học Tập - Vật Lý & Tuổi Trẻ Việt Nam")
st.caption("Tác giả: **Hoàng Lân** • Chatbot AI hỗ trợ học tập và khám phá khoa học bằng tiếng Việt 🇻🇳")

# 🔑 API Key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 💬 Lưu hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập chat
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gọi OpenAI để sinh phản hồi
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 📷 Ảnh tác giả (hiển thị góc phải)
author_image_url = "https://drive.google.com/uc?export=view&id=1vCLYkeFL1ZgcJwvD_FYw2BeQbP7Wuf69"
st.markdown(f'<img src="{author_image_url}" class="avatar">', unsafe_allow_html=True)

# 🧾 Footer
st.markdown('<div class="footer">© 2025 Hoàng Lân • Chatbot học tập Vật Lý</div>', unsafe_allow_html=True)
