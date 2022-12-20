import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Рекомендации")
st.write("реки")

VKdf = pd.read_excel('posts.xlsx', sheet_name='РГООИ_Надежда_')
VKdf['only_date'] = VKdf['date'].dt.strftime('%Y-%m')
VKdf['only_time'] = VKdf['date'].dt.strftime('%H')
VKdf['weekday'] = VKdf['date'].dt.dayofweek
months = pd.date_range('2022-01-03', '2022-09-01', freq='1M', normalize=True)
months_to_analyse = [d.strftime('%Y-%m') for d in months]
vk2022 = VKdf.loc[VKdf['only_date'].isin(months_to_analyse)]
st.dataframe(VKdf.describe())


st.header("Разработчики")
st.write("""[Колеух Максим](https://vk.com/kelchel) - \n
[Иван Гречкин](https://vk.com/yokore) - \n
[Егор Мацко](https://vk.com/kitsunnet) - \n
[Вадим Игнатов](https://vk.com/qbubble) - \n
[Николай Сергиенко](https://vk.com/waflyaaa) -
""")