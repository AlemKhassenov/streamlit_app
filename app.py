import streamlit as st
import pandas as pd
import requests

# Заголовок
st.title("Индивидуальный план развития ученика")

# Форма для ввода данных
with st.form("student_form"):
    name = st.text_input("ФИО ученика")
    student_class = st.text_input("Класс")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    grade = st.number_input("Оценка (по 5-балльной шкале)", min_value=1, max_value=5, step=1)
    submit_button = st.form_submit_button("Создать таблицу")

if submit_button and name and student_class and subject:
    # Создание таблицы с бинарными показателями
    columns = ["Понимание темы", "Применение знаний", "Анализ", "Критическое мышление", "Творческое решение"]
    df = pd.DataFrame([[0] * len(columns)], columns=columns)
    df_editor = st.data_editor(df, num_rows="fixed")
    
    if st.button("Отправить данные в AI"):
        data = {
            "name": name,
            "class": student_class,
            "subject": subject,
            "grade": grade,
            "results": df_editor.to_dict(orient="records")[0]
        }
        
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
