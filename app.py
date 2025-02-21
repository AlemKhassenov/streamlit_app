import streamlit as st
import pandas as pd
import requests
import io
import os
from docx import Document

# Загружаем API-ключ из переменной окружения
API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка API-ключа
if not API_KEY:
    st.error("Ошибка: API-ключ не найден. Добавьте его в переменные среды или GitHub Secrets.")
    st.stop()

def load_data_from_google_sheets(sheet_url, student_name):
    export_url = "https://docs.google.com/spreadsheets/d/1BeXPi5LRSIj0xDjGZjey0VfBU08mnjJm/export?format=csv"
    
    df = pd.read_csv(export_url)
    
    # Выводим названия всех столбцов, чтобы понять, как записан "ФИО"
    st.write("Названия столбцов в Google Sheets:", df.columns.tolist())

    # Попробуем исправить возможные ошибки в названии столбца
    df.columns = df.columns.str.strip()  # Убираем пробелы в начале и конце
    df.columns = df.columns.str.replace("\t", "")  # Убираем табуляции

    # Проверим правильное название
    if "ФИО" not in df.columns:
        st.error("Ошибка: В таблице нет столбца 'ФИО'. Проверьте названия столбцов.")
        return None

    student_data = df[df["ФИО"] == student_name]
    
    if student_data.empty:
        return None
    
    student_data_json = student_data.to_json(orient="records")
    return student_data_json


# Функция для отправки данных через API ChatGPT
def send_data_to_api(student_data, prompt):
    api_url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    final_prompt = f"{prompt}\n\nДанные ученика:\n{student_data}"

    payload = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": final_prompt}],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Ошибка API: {response.status_code}, {response.text}"

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
    student_class = st.selectbox("Класс", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])
    subject = st.selectbox("Предмет", ["Математика", "Физика", "Химия", "Биология", "Английский язык"])
    grade = st.number_input("Текущая оценка из EduPage, округленная до целых", min_value=0, max_value=100, step=1, value=0)
    submit_button = st.form_submit_button("Сформировать ПИР")

if submit_button:
    student_data = load_data_from_google_sheets("https://docs.google.com/spreadsheets/d/1BeXPi5LRSIj0xDjGZjey0VfBU08mnjJm/export?format=csv", name)
    
    if student_data is None:
        st.error("Ошибка: Данные ученика не найдены!")
    else:
        st.write("Данные найдены, отправляются на анализ...")
        
        # Промпт для ChatGPT
        prompt = """
Учащийся проходил обучение по различным темам. В столбцах приведены ожидания от обучения (цели), а в последней строке указано:
- 1 = ученик достиг цели.
- 0 = ученик не достиг цели.

Проанализируй, какие темы усвоены хорошо, а какие требуют доработки.  
Определи, какие пробелы в знаниях есть у ученика, и предложи **рекомендации**.  
Для каждой недостигнутой цели (0) предложи **ресурсы для изучения**: 
- **Ссылки на видео (YouTube, Coursera, Khan Academy и т. д.)**  
- **Книги / статьи / курсы**  

Данные для анализа:  
{student_data}
"""
        api_response = send_data_to_api(student_data, prompt)
        
        if "Ошибка" in api_response:
            st.error(api_response)
        else:
            doc_buffer = create_docx(name, student_class, subject, grade, api_response)
            st.download_button("📄 Скачать отчет (DOCX)", data=doc_buffer, file_name=f"ПИР_{name}_{grade}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            st.success("Отчет сформирован! Вы можете скачать его.")
