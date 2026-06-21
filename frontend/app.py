import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

st.title("ИИ-ассистент")

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header(" Информация")
    st.write(f"**Ваш ID:** {st.session_state.user_id[:8]}...")
    
    if st.button(" Очистить историю"):
        try:
            response = requests.post(
                "http://localhost:8000/clear",
                json={"user_id": st.session_state.user_id}
            )
            if response.status_code == 200:
                st.session_state.messages = []
                st.success("История очищена!")
                st.rerun()
            else:
                st.error("Ошибка при очистке")
        except Exception as e:
            st.error(f"Ошибка: {e}")
    
    st.divider()
    st.caption("API: http://localhost:8000/docs")
    st.caption("Бесплатный ИИ (Pollinations)")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Напишите сообщение..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            try:
                response = requests.post(
                    "http://localhost:8000/ask",
                    json={"user_id": st.session_state.user_id, "prompt": prompt},
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data["response"]
                    st.write(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Ошибка API: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(" Не удалось подключиться к серверу.\nУбедитесь, что бэкенд запущен.")
            except requests.exceptions.Timeout:
                st.error(" Превышено время ожидания ответа от сервера.")
            except Exception as e:
                st.error(f" Ошибка: {e}")