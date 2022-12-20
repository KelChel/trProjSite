import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Рекомендации")
st.write("реки")

VKdf = pd.read_excel('posts.xlsx', sheet_name='РГООИ_Надежда_')


st.header("Разработчики")
st.write("""[Колеух Максим](https://vk.com/kelchel) - \n
[Иван Гречкин](https://vk.com/yokore) - \n
[Егор Мацко](https://vk.com/kitsunnet) - \n
[Вадим Игнатов](https://vk.com/qbubble) - \n
[Николай Сергиенко](https://vk.com/waflyaaa) -
""")