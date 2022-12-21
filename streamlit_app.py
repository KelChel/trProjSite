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

workday_df_not_rush = vkdf.loc[(vkdf['weekday'].isin(list(range(0, 5)))) & (vkdf['only_time'].isin(['09','10','16','17','18','19','20',]))]
workday_df_not_rush['only_time'].unique()


median_activity = workday_df_not_rush.groupby('only_time').agg('median').reset_index()
length_count_time = workday_df_not_rush.groupby('only_time')['count'].sum().reset_index()
fig, ax = plt.subplots(figsize = (8, 4))
for activity in ['comments', 'likes', 'reposts']: 
    plt.plot(median_activity['only_time'], median_activity[activity], label = activity)
plt.plot(length_count_time['only_time'], length_count_time['count'], label = 'count')
plt.xticks(list(median_activity['only_time'].unique()))
plt.title('Средние значения активностей посетилей паблика по времени публикации в будни не в часы пик')
plt.xlabel('Время публикации, час')
plt.ylabel('Количество единиц активности')
plt.xticks(rotation=45)
plt.legend()
st.pyplot()

length_count = workday_df_not_rush.groupby('text_length')['count'].sum().reset_index()
length_grouped = workday_df_not_rush.groupby('text_length').agg('median').reset_index()
fig, ax = plt.subplots(figsize = (8, 4))
for activity in ['comments', 'likes', 'reposts']: 
    plt.plot(length_grouped['text_length'], length_grouped[activity], label = activity)
plt.plot(length_count['text_length'], length_count['count'], label = 'count')
plt.title('Средние значения активностей посетилей паблика по длине текста')
plt.xlabel('Длина текста')
plt.ylabel('Количество активностей')
plt.xticks(rotation=45)
plt.legend()
st.pyplot()

attachments = workday_df_not_rush.groupby('media 1').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index()
attachments.sort_values('likes')

workday_rush = vkdf.loc[(vkdf['weekday'].isin(list(range(0, 5)))) & (vkdf['only_time'].isin(['11','12','13','14','15']))]
median_activity = workday_rush.groupby('only_time').agg('median').reset_index()
length_count_time = workday_rush.groupby('only_time')['count'].sum().reset_index()
fig, ax = plt.subplots(figsize = (8, 4))
for activity in ['comments', 'likes', 'reposts']: 
    plt.plot(median_activity['only_time'], median_activity[activity], label = activity)
plt.plot(length_count_time['only_time'], length_count_time['count'], label = 'count')
plt.xticks(list(median_activity['only_time'].unique()))
plt.title('Средние значения активностей посетилей паблика по времени публикации в часы-пик')
plt.xlabel('Время публикации, час')
plt.ylabel('Количество единиц активности')
plt.xticks(rotation=45)
plt.legend()
st.pyplot()

attachments = workday_rush.groupby('media 1').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index()
attachments.sort_values('likes')

weekend_df = vkdf.loc[(vkdf['weekday'].isin(list(range(5, 7))))]

median_activity = weekend_df.groupby('only_time').agg('median').reset_index()
length_count_time = weekend_df.groupby('only_time')['count'].sum().reset_index()
fig, ax = plt.subplots(figsize = (8, 4))
for activity in ['comments', 'likes', 'reposts']: 
    plt.plot(median_activity['only_time'], median_activity[activity], label = activity)
plt.plot(length_count_time['only_time'], length_count_time['count'], label = 'count')
plt.xticks(list(median_activity['only_time'].unique()))
plt.title('Средние значения активностей посетилей паблика по времени публикации в выходные')
plt.xlabel('Время публикации, час')
plt.ylabel('Количество единиц активности')
plt.xticks(rotation=45)
plt.legend()
st.pyplot()

length_count = weekend_df.groupby('text_length')['count'].sum().reset_index()
length_grouped = weekend_df.groupby('text_length').agg('median').reset_index()
fig, ax = plt.subplots(figsize = (8, 4))
for activity in ['comments', 'likes', 'reposts']: 
    plt.plot(length_grouped['text_length'], length_grouped[activity], label = activity)
plt.plot(length_count['text_length'], length_count['count'], label = 'count')
plt.title('Средние значения активностей посетилей паблика по длине текста в выходные')
plt.xlabel('Длина текста')
plt.ylabel('Количество активностей')
plt.xticks(rotation=45)
plt.legend()
st.pyplot()


st.header("Разработчики")
st.write("""[Колеух Максим](https://vk.com/kelchel) - сайт\n
[Иван Гречкин](https://vk.com/yokore) - анализ и рекомендации\n
[Егор Мацко](https://vk.com/kitsunnet) - \n
[Вадим Игнатов](https://vk.com/qbubble) - \n
[Николай Сергиенко](https://vk.com/waflyaaa) -
""")