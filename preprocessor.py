import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?[ap]m\s-\s'

    # Split the data into messages and dates
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    # Correct column name
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
# Convert message_date type
    # Remove leading/trailing spaces
    df['message_date'] = df['message_date'].str.strip()
    df['message_date'] = pd.to_datetime(
        df['message_date'], format='%d/%m/%Y, %I:%M %p -', errors='coerce')

# Optionally rename the column if needed
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # df.head()
    users = []
    messages = []

    for message in df['user_message']:
        # Attempt to split the message into a user and the actual message
        # maxsplit=1 ensures we only split on the first colon
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)

        if len(entry) > 2:  # Check if we successfully split into user and message
            users.append(entry[1])  # Append the username
            messages.append(entry[2])  # Append the actual message
        else:
            # If the message doesn't match the format, assign 'Unknown' user
            users.append('Unknown')
            messages.append(message)  # Keep the full message as is

# Add the extracted users and messages to the DataFrame
    df['user'] = users
    df['message'] = messages

# Drop the original 'user_message' column
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
