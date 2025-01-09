import streamlit as st
import pandas as pd
import numpy as np

# Настройка заголовка страницы
st.title('Моё первое Streamlit приложение')

# Добавление текста
st.write('Привет! Это простой пример приложения Streamlit.')

# Создание боковой панели
st.sidebar.header('Настройки')
user_input = st.sidebar.text_input('Введите ваше имя', 'Гость')
st.write(f'Привет, {user_input}!')

# Создание графика
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)
st.line_chart(chart_data)

# Добавление виджетов
if st.checkbox('Показать датафрейм'):
    st.write(chart_data)

# Добавление селектора
option = st.selectbox(
    'Выберите число',
    [1, 2, 3, 4, 5]
)
st.write(f'Вы выбрали: {option}')

# Добавление слайдера
values = st.slider(
    'Выберите диапазон',
    0.0, 100.0, (25.0, 75.0)
)
st.write(f'Значения: {values}')