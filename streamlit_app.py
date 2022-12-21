import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re


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

def find_topic(text): 
    regular = r'#\S+'
    compiled = re.compile(regular)
    try: 
        lst_topics = compiled.findall(text)
    except BaseException: 
        lst_topics = ['No topic']
    return lst_topics
vk2022['topics'] = vk2022.apply(lambda row : find_topic(row['text']), axis=1)

def word_count(textik): 
    lst = str(textik).split()
    return len(lst)
vk2022['text_length'] = vk2022.apply(lambda row : word_count(row['text']), axis=1)
vk2022['count'] = 1

vk2022_exploded = vk2022.explode('topics')

vkdf = vk2022
vkexp_df = vk2022_exploded

def text_group_by_count(textt):
    if textt < 50:
        return 50
    elif textt >= 50 and textt < 100:
        return 100 
    elif textt >= 100 and textt < 150:
        return 150 
    elif textt >= 150 and textt < 200:
        return 200 
    elif textt >= 200 and textt < 250:
        return 250 
    else:
        return 300 
    
vkdf['text_length'] = vkdf.apply(lambda row : text_group_by_count(row['text_length']), axis=1)

st.dataframe(vkdf.describe())



st.header("Разработчики")
st.write("""[Колеух Максим](https://vk.com/kelchel) - \n
[Иван Гречкин](https://vk.com/yokore) - \n
[Егор Мацко](https://vk.com/kitsunnet) - \n
[Вадим Игнатов](https://vk.com/qbubble) - \n
[Николай Сергиенко](https://vk.com/waflyaaa) -
""")