streamlit
pandas
requests
openpyxl
python-docx

import streamlit as st

# Функция для установки фонового изображения
def set_background(image_url):
    page_bg = f"""
    <style>
    .stApp {{
        background: url("{image_url}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# Укажите ссылку на фоновое изображение
background_image_url = "https://images.pexels.com/photos/30388784/pexels-photo-30388784.jpeg?auto=compress&cs=tinysrgb&w=1200&lazy=load"  # Можно заменить на свое изображение
set_background(background_image_url)

# Заголовок
st.title("Индивидуальный план развития ученика Quantum STEM School")

# Форма для ввода данных
with st.form("student_form"):
    name = st.text_input("ФИО ученика")
    student_class = st.text_input("Класс")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    
    # Исправленный number_input
    grade = st.number_input("Текущая оценка из EduPage, округленная до целых", min_value=0, max_value=100, step=1, value=0)

    uploaded_file = st.file_uploader("Загрузите Excel-файл с ожидаемыми результатами", type=["xls", "xlsx"])
    
    # Добавление кнопки отправки
    submit_button = st.form_submit_button("Сформировать ПИР")

if submit_button:
    st.success("Форма успешно отправлена!")
