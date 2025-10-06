import streamlit as st
from openai import OpenAI

# Tiêu đề & mô tả
st.title("💬 Chatbot Học Tập")
st.write(
    "Đây là chatbot đơn giản dùng mô hình GPT của OpenAI để trò chuyện. "
    "Bạn không cần nhập API key nếu chủ app đã cài sẵn trong `Secrets`. "
    "Nếu muốn lấy key riêng, xem hướng dẫn [tại đây](https://platform.openai.com/account/api-keys)."
)

# 🔑 Lấy API key từ Secrets (đã cài trong Streamlit Cloud)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Lưu lịch sử hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập chat
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):

    # Lưu & hiển thị tin nhắn người dùng
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

    # Ghi phản hồi ra giao diện
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    # Lưu phản hồi vào session
    st.session_state.messages.append({"role": "assistant", "content": response})
