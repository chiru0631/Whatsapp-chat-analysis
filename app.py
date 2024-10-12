import streamlit as st
import preprocessor as preprocessor
import helper as helper
import matplotlib.pyplot as plt

# Title and Author Information
st.markdown("<h1 style='text-align: center; font-size: 36px;'>Whatsapp Chat Analyzer</h1>",
            unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Developed by: <b>Chirag Sathish</b></h2>",
            unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'><a href='www.linkedin.com/in/chirag-sathish-87b846271' target='_blank'>LinkedIn Profile</a> | 📧 <a href='mailto:chiru7975@gmail.com'>Email me</a></h4>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Welcome to Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)  # Using preprocessor directly

    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('Unknown')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis of", user_list)

    st.header('TOP STATS')

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, links = helper.fetch_stats(
            selected_user, df)

        st.header("Links")
        st.dataframe(links)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Messages")
            st.title(num_media_messages)
        with col4:
            st.header("Number of Links")
            st.title(len(links))

        # Monthly Timeline
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title('Daily Timeline')
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            if not busy_day.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            else:
                st.write("No activity data available for the selected user.")

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            if not busy_month.empty:
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            else:
                st.write("No activity data available for the selected user.")

        # Busiest User Analysis (for group chats)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.title("Percentage")
                st.dataframe(new_df)

        # WordCloud
        df_wc = helper.create_wordcloud(selected_user, df)
        st.title('Wordcloud')
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            st.title('Pie Chart')
            if not emoji_df.empty:
                fig, ax = plt.subplots()
                ax.pie(emoji_df[1].head(),
                       labels=emoji_df[0].head(), autopct="%0.2f")
                st.pyplot(fig)
            else:
                st.write("No emojis found to display in the pie chart.")
