import streamlit as st
import pandas as pd
import requests
import io

# Заголовок
st.title("Индивидуальный план развития ученика")

# Форма для ввода данных
with st.form("student_form"):
    name = st.text_input("ФИО ученика")
    student_class = st.text_input("Класс")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    grade = st.number_input("Оценка (по 100-балльной шкале)", min_value=1, max_value=5, step=1)
    uploaded_file = st.file_uploader("Загрузите Excel-файл", type=["xls", "xlsx"])
    submit_button = st.form_submit_button("Отправить файл в ChatGPT")

        
        # Отправка данных в API
        response = requests.post("https://your-api-endpoint.com/generate_plan", json=data)
        
        if response.status_code == 200:
            plan_url = response.json().get("plan_url")
            st.success("План успешно создан!")
            st.markdown(f"[Скачать план]({plan_url})")
        else:
            st.error("Ошибка при генерации плана")

# Дополнительный функционал: отображение предыдущих планов
if "history" not in st.session_state:
    st.session_state.history = []

if plan_url:
    st.session_state.history.append({
        "ФИО": name,
        "Класс": student_class,
        "Предмет": subject,
        "Оценка": grade,
        "Ссылка": plan_url
    })

if st.session_state.history:
    st.subheader("История созданных планов")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
