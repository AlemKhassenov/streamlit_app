import streamlit as st
import pandas as pd
import requests
import io
import docx
from docx import Document

# Функция для отправки файла через API ChatGPT
def send_file_to_api(file, prompt):
    api_url = "https://api.openai.com/v1/chat/completions"  # Укажите ваш API-адрес
    api_key = "A"  # Замените на ваш API-ключ

    if api_key == "YOUR_API_KEY":
        return "Ошибка: API-ключ не установлен!"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        # Читаем содержимое файла
        file_content = file.getvalue()

        # Преобразуем Excel в DataFrame
        df = pd.read_excel(io.BytesIO(file_content))

        # Преобразуем DataFrame в JSON-строку
        file_data = df.to_json(orient="records")

        # Формируем промпт
        final_prompt = f"{prompt}\n\nДанные из файла:\n{file_data}"

        payload = {
            "model": "gpt-4",
            "messages": [{"role": "user", "content": final_prompt}]
        }

        response = requests.post(api_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Ошибка API: {response.status_code}, {response.text}"
    
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети: {e}"
    except Exception as e:
        return f"Ошибка обработки данных: {e}"

# Функция для создания DOCX-файла
def create_docx(student_name, student_class, subject, grade, gpt_response):
    doc = Document()
    
    doc.add_heading("Индивидуальный план развития ученика", level=1)

    doc.add_paragraph(f"ФИО ученика: {student_name}")
    doc.add_paragraph(f"Класс: {student_class}")
    doc.add_paragraph(f"Предмет: {subject}")
    doc.add_paragraph(f"Текущая оценка: {grade}")

    doc.add_heading("Анализ и рекомендации", level=2)
    doc.add_paragraph(gpt_response)

    # Сохранение файла в буфер
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    
    return buffer

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
background_image_url = "https://images.pexels.com/photos/30388784/pexels-photo-30388784.jpeg?auto=compress&cs=tinysrgb&w=1200&lazy=load"
set_background(background_image_url)

# Заголовок
st.title("Индивидуальный план развития ученика Quantum STEM School")

# Форма для ввода данных
with st.form("student_form"):
    name = st.text_input("ФИО ученика")
    student_class = st.text_input("Класс")
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    
    grade = st.number_input("Текущая оценка из EduPage, округленная до целых", min_value=0, max_value=100, step=1, value=0)

    uploaded_file = st.file_uploader("Загрузите Excel-файл с ожидаемыми результатами", type=["xls", "xlsx"])
    
    submit_button = st.form_submit_button("Сформировать ПИР")

if submit_button:
    if uploaded_file is None:
        st.error("Ошибка: Пожалуйста, загрузите Excel-файл!")
    else:
        st.write("Файл успешно загружен, отправляется на анализ...")

        # Промпт для ChatGPT
        prompt = "Проанализируй файл, выяви сильные и слабые стороны, напиши рекомендации."

        # Отправка файла в API и получение ответа
        api_response = send_file_to_api(uploaded_file, prompt)

        # Проверка на ошибки в API-ответе
        if "Ошибка" in api_response:
            st.error(api_response)
        else:
            # Создание DOCX-файла
            doc_buffer = create_docx(name, student_class, subject, grade, api_response)

            # Кнопка для скачивания файла
            st.download_button(
                label="📄 Скачать отчет (DOCX)",
                data=doc_buffer,
                file_name=f"ИПР_{name}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

            st.success("Отчет сформирован! Вы можете скачать его.")

