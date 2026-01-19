import re
import pandas as pd

def preprocess(data):
    #Theee pattern
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    #split of message and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'message_dates': dates})

    #convert to date_time
    df['message_dates'] = pd.to_datetime(df['message_dates'], format=r'%d/%m/%y, %H:%M - ')

    #split of user and messages
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_messages'], inplace=True)

    #new date,year,month_name,day,day_name,hour.min columns added
    df['only_date'] = df['message_dates'].dt.date
    df['year'] = df['message_dates'].dt.year
    df['month_num'] = df['message_dates'].dt.month
    df['month'] = df['message_dates'].dt.month_name()
    df['day'] = df['message_dates'].dt.day
    df['day_name'] = df['message_dates'].dt.day_name()
    df['hour'] = df['message_dates'].dt.hour
    df['minute'] = df['message_dates'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str("00"))
        elif hour == 0:
            period.append(str("00") + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))
    df['period'] = period

    return df