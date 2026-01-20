import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    


    #fetching unique users assssss
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,media_messages,links_shared = helper.fetch_stats(selected_user, df)


        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(media_messages)

        with col4:
            st.header("Links Shared")
            st.title(links_shared)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.fill_between(timeline['time'], timeline['message'], color='#2ecc71', alpha=0.3)
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        d_timeline = helper.daily_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(d_timeline['only_date'],d_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Weekly activity map
        st.title("Weekly Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busiest Day")
            busy_day = helper.weekly_activity(selected_user, df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busiest Month")
            busy_month = helper.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='grey')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        #Activity Heatmap
        st.title("Weekly Activity Map")
        act_heatmap = helper.activity_heatmap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(act_heatmap,cmap='YlGnBu')
        st.pyplot(fig)




        #finding the busiest person

        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x,new_df= helper.most_busy_users(df)
            fig,ax = plt.subplots()

            col1 , col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='grey')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        #Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most Common Words
        st.title("Most Common Words")
        most_common = helper.most_common_words(selected_user, df)

        fig,ax = plt.subplots()
        ax.barh(most_common['Word'],most_common['Counts'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Emoji Analysis
        col1, col2 = st.columns(2)
        emoji_df = helper.emoji_count(selected_user, df)
        plt.rcParams['font.family'] = ['Segoe UI Emoji', 'Apple Color Emoji', 'DejaVu Sans']
        with col1:
            st.subheader("Emoji Frequency")
            st.dataframe(emoji_df)
        with col2:
            st.subheader("Chart Analysis")
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


