from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1.Number of messages of group
    num_messages = df.shape[0]

    # 2.Number of words of group
    words = []
    for messages in df['message']:
        words.extend(messages.split())



    # 3.Number of media shared
    media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4.Number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))


    return num_messages, len(words),media_messages,len(links)

# 5.Busy Users
def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'Name', 'count': 'Percent'})
    return x,new_df

# 6.Word Cloud
def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['message']!='<Media omitted>\n']

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

# 7.Most Common Words
def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        words.extend(message.split())

    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Counts'])

# 8. Emoji Count

def emoji_count(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

# 9.Monthly_Timeline

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

# 10.Daily_Timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    d_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return d_timeline

#11.Weekly Activity Map

def weekly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

#12.Monthly Activity Map

def monthly_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

#13.Activity Heatmap

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    act_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return  act_heatmap