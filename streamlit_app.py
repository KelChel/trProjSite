import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re


st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Рекомендации [группе VK](https://vk.com/rgooinadezhda)")

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
time_grouped = vkdf.groupby('only_time').agg('sum').reset_index()

st.dataframe(time_grouped)

st.write('Не в час пик количество постов самое высокое в 10 и 16 часов и активность тоже примерно одинаковая. А вот репостов больше в 18. Может быть, если нужно больше лайков, стоит тоже побольше публиковать в 10 и 16 часов? А для репостов - в 18')

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

st.write('Активность хуже всего при длине текстов от 50 до 100 слов. Чем больше текста, тем выше активность')

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

st.write('Пожалуй, стоит обратить внимание на посты с фото, либо где есть смешанный формат вложений - такие хорошо лайкают. Да и в целом это очевидно и без текущего исследования и все посты имеют вложения в видео картинок либо видео')

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

st.write("""Cамая большая активность пользователей - в обед, особенно в 12 часов дня. В 14 часов дня, хоть и повышается частота выхода постов, рост активности не превышает значение активность в 12 часов.
Что касается длины текстов, которые публикуются в часы пик, лучше репостят тексты от 250 слов, хоть и в малом количестве, а лайкают лучше тексты от 200 и от 300 слов, как и говорилось раннее, по статистике, чем больше слов - тем больше лайков, с комментариями же дело обстоит также, как и не в час пик, большинство обсуждений приходится на текста от 200 слов. При этом большинство текстов - до 150 слов. Вывод: если нужны лайки - золотая середины - от 300 слов. Если репосты - можно держать ту же планку, но немного опустив до 250. Самые обсуждаемые, как и говорилсь тексты с количеством слов - 200. Итого, наибольшую активность вызывают посты от 200 до 300 слов.""")

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

st.write("""1. Интересно, что значения активности крайне не стабильные, в 10 и 13 часов были пики активности, после которых были резкие спады. На 15 часах хоть количество постов и возрастало, на активность в положительную сторону это не влияло, соответственно, в выходные дни люди проявляли больше активности к постам, которые выходили в 10 и 13 часов, в промежутке между ними активность падала, но была стабильной.
2. Тут уже тексты от 100 слов практически такие же популярные как и тексты от 300 слов по лайкам, более бурные обсуждения же вызывали посты значением в 250 слов, а потом, по мере увеличения размерности текста активность обсуждений немного спадала, но не до критического уровня, как до этого. Но вместе с тем падала и частота выхода постов.
В целом, стоит оставить текующее время выхода постов, но можно больше сконцентрироваться на их количестве в промежутке от 10 до 13 часов
И публиковать лучше тексты до 100 слов. А также увеличить количество постов с 250+ словами, так как даже при своём малом количестве они вызывают высокую активность""")

attachments1 = weekend_df.groupby('media 1').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index()
attachments1.sort_values('likes')

topics_sorted = vkexp_df['topics'].value_counts()[vkexp_df['topics'].value_counts(normalize=True) > 0.01]

vkexp_df['topics'] = vkexp_df['topics'].str.lower()
topics_sorted1 = vkexp_df['topics'].value_counts()[vkexp_df['topics'].value_counts(normalize=True) > 0.01]  


top_topics = list(topics_sorted1.index)
vk_pop_topics = vkexp_df.loc[vkexp_df['topics'].isin(top_topics)]

vk_pop_topics.groupby('topics').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index().sort_values(by='likes', ascending=False)

vk_pop_topics_weekday = vk_pop_topics.loc[(vk_pop_topics['weekday'].isin(list(range(0, 5))))]
st.dataframe(vk_pop_topics_weekday.groupby('topics').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index().sort_values(by='likes', ascending=False))


st.write("""Кажется, что топиков: #интегративныйлагерь, #кабардинканадеждикус, #летнийлагерь, #море, #островокнадежды, #отдых - хорошо лайкают и репостят. На них и нужно обратить внимание, но насколько я понимаю, все они завязаны на летнем отдыхе, что актуально лишь в лентее время. Поэтому стоит обратить внимание на возможно не сезонные топики по типу #подопечныенадежды, #добраясреда, #благотворительность, #ростовнадону. Посты без топика же поддерживаются достаточно скудную активность, но в целом, их не так уж и много.""")


vk_pop_topics_weekend = vk_pop_topics.loc[(vk_pop_topics['weekday'].isin(list(range(5, 7))))]
st.dataframe(vk_pop_topics_weekend.groupby('topics').agg({'likes' : 'median', 'reposts' : 'median', 'media count' : 'median', 'count' : 'sum'}).reset_index().sort_values(by='likes', ascending=False))


st.write("""Топики про отдых также остаются популярными в будни, а вот в выходные дни всё меняются, популярными топиками становятся #подопечныенадежды, #добраясреда, #ростовнадону, #детитакнеделятся, соответсвенно стоит обратить особое внимание на подобные топики в выходные дни, так как даже при своём малом количестве они имеют высокое количество лайков и репостов(кроме топика #добрая среда)""")
st.header("Разработчики")
st.write("""[Колеух Максим](https://vk.com/kelchel) - студент провёл работу по сбору датасета и реализации сайта с помощью языка Python\n
[Иван Гречкин](https://vk.com/yokore) - студент дал рекомендации на основе проанализированных данных, а также провёл обработку датасета\n
[Егор Мацко](https://vk.com/kitsunnet) - студент провёл анализ данных и работу по сбору и подготовке датасета к обработке данных.\n
[Вадим Игнатов](https://vk.com/qbubble) - студент провёл анализ данных, так же помогал при подготовке датасета к обработке данных\n
[Николай Сергиенко](https://vk.com/waflyaaa) - студент проделал работу по сбору датасета, а также оказал помощь в реализации сайта на Python и написании отчёта
""")