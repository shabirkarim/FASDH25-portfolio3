import pandas as pd
import plotly.express as px


# Load the dataset
file_path = '../data/dataframes/length/length.csv'
df = pd.read_csv(file_path)

# Check the first few rows to understand the structure
print("First few rows of the dataset:")
print(df.head())

# convert the year, month, and day columns to datetime (if they are not already)
# combining year, month, and day to create a proper date
# code adapted with the help of CHATGPT check Solution GPT 1.1
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# group the data by the date and count the articles published each day
articles_per_day = df.groupby('date').size().reset_index(name='article_count')

#  sort the data by date from old year to new year
articles_per_day = articles_per_day.sort_values(by='date', ascending=True)

# display the result
print("\nNumber of articles published each day:")
print(articles_per_day)

# plot a bar chart to visualize the number of articles published each day
fig = px.bar(articles_per_day, 
             x='date', 
             y='article_count', 
             title="Number of Articles Published Each Day", 
             labels={'date': 'Publication Date', 'article_count': 'Number of Articles'})
# show the plot
fig.show()

"""So far after plotting Bar chart I saw the articles published from 2017 to 2021 are very less, so there are insignificant,
consider them to remove in final presentation script to create clear visuals"""

# calculate the average article length per month or year, here we will do monthly
# Code adapted from chatgpt check Solution 1.2
avg_article_length = df.groupby(['year', 'month'])['length'].mean().reset_index()
print("\nAverage article length calculated per year and month:")
print(avg_article_length.head())

#sort the data by date from old year to new year
avg_article_length = avg_article_length.sort_values(by=['year', 'month'], ascending=True)
# print avg article length
print(avg_article_length.head())

# create a new column combining year and month for easier plotting
# Code adapted from chatgpt check Solution 1.3
avg_article_length['Year-Month'] = avg_article_length['year'].astype(str) + '-' + avg_article_length['month'].astype(str)
# print the results
print(avg_article_length[['Year-Month', 'length']].head())

# plot a line chart to show the trend of article length over time
fig = px.line(avg_article_length, 
              x='Year-Month', 
              y='length', 
              title="Trend of Article Length Over Time", 
              labels={'Year-Month': 'Year-Month', 'length': 'Average Article Length'},
              markers=True)
# show the plot
fig.show()

"""So far after plotting Bar chart I saw the articles published from 2017 to 2021 are very less, so there are insignificant,
consider them to remove in final presentation script to create clear visuals"""

# Plot a bar chart to show the average article length by Year-Month
fig_bar = px.bar(avg_article_length, 
                 x='Year-Month', 
                 y='length', 
                 title="Average Article Length by Year-Month", 
                 labels={'Year-Month': 'Year-Month', 'length': 'Average Article Length'},
                 color='length')  # Color the bars based on article length

# Show the plot
fig_bar.show()

"""So far after plotting Bar chart I saw the articles published from 2017 to 2021 are very less, so there are insignificant,
consider them to remove in final presentation script to create clear visuals"""













