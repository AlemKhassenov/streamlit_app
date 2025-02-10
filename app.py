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
background_image_url = "https://images.unsplash.com/photo-1738705466275-1f94be26c5bd?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxmZWF0dXJlZC1waG90b3MtZmVlZHw2Mnx8fGVufDB8fHx8fA%3D%3D"  # Можно заменить на свое изображение
set_background(background_image_url)

# Заголовок
st.title("Индивидуальный план развития ученика")

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
