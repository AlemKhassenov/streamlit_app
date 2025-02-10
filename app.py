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
    grade = st.number_input("Оценка (по 100-балльной шкале)", min_value=1, max_value=100, step=0.1)
    uploaded_file = st.file_uploader("Загрузите файл", type=["xls", "xlsx"])
    submit_button = st.form_submit_button("Сформировать ПИР")

# Функция для отправки файла по API
def send_file_to_api(file, prompt):
    api_url = "https://api.openai.com/v1/chat/completions"  # Укажите ваш API-адрес
    api_key = "YOUR_API_KEY"  # Замените на ваш API-ключ

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

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
        return f"Ошибка: {response.status_code}, {response.text}"

# Если пользователь загрузил файл и нажал кнопку
if submit_button and uploaded_file is not None:
    st.write("Файл успешно загружен и отправляется на обработку...")
    
    # Пример промпта (можно изменить на свой)
    prompt = "Проанализируйте данные из Excel-файла и сформируйте индивидуальный план развития ученика."
    
    # Отправка файла в API и получение ответа
    api_response = send_file_to_api(uploaded_file, prompt)
    
    # Вывод ответа
    st.subheader("Ответ от ChatGPT:")
    st.write(api_response)
