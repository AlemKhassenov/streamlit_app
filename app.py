import streamlit as st

st.title("Индивидуальный план развития ученика")

# Форма для ввода данных
with st.form("student_form"):
    name = st.text_input("ФИО ученика")
    student_class = st.text_input("Класс")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    
    # Исправленный number_input
    grade = st.number_input("Оценка (по 100-балльной шкале)", min_value=0, max_value=100, step=1, value=0)

    uploaded_file = st.file_uploader("Загрузите Excel-файл с ожидаемыми результатами", type=["xls", "xlsx"])
    
    # Добавление кнопки отправки
    submit_button = st.form_submit_button("Сформировать ПИР")

if submit_button:
    st.success("Форма успешно отправлена!")
