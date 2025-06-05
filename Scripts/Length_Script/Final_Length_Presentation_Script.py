# import necessary libraries
import pandas as pd
import plotly.express as px

# load the dataset
file_path = '../data/dataframes/length/length.csv'
df = pd.read_csv(file_path)

# check the first few rows to understand the structure
print("First few rows of the dataset:")
print(df.head())

# convert the year, month, and day columns to datetime
# code adapted with the help of CHATGPT check Solution GPT 1.1
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# filter out the data from 2017 to May 2021
df = df[df['date'] >= '2021-05-01']  # Keep data after May 2021 and including May 2021

# group the data by the date and count the articles published each day
articles_per_day = df.groupby('date').size().reset_index(name='article_count')

# sort the data by date from old year to new year
articles_per_day = articles_per_day.sort_values(by='date', ascending=True)

# plot a bar chart to visualize the number of articles published each day
fig = px.bar(articles_per_day, 
             x='date', 
             y='article_count', 
             title="Number of Articles Published Each Day", 
             labels={'date': 'Publication Date', 'article_count': 'Number of Articles'},
             color='article_count',  # Adding color for visual distinction
             color_continuous_scale='Viridis')  # Choosing a color scale

# add annotations to highlight trends or specific days if needed
# Code adapted with the help of chatgpt, check Solution GPT 1.4
fig.add_annotation(
    x=articles_per_day['date'].iloc[0], 
    y=articles_per_day['article_count'].max(),
    text="Start of analysis",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

fig.show()

# Save the plot to an HTML file
fig.write_html("../Visuals/Final_Visuals/Length_final_visuals/articles_per_day.html")

# calculate the average article length per month or year (monthly in this case)
avg_article_length = df.groupby(['year', 'month'])['length'].mean().reset_index()

# sort the data by date from old year to new year
# Code adapted from chatgpt check Solution 1.2
avg_article_length = avg_article_length.sort_values(by=['year', 'month'], ascending=True)

# create a new column combining year and month for easier plotting
# Code adapted from chatgpt check Solution 1.3
avg_article_length['Year-Month'] = avg_article_length['year'].astype(str) + '-' + avg_article_length['month'].astype(str)

# plot a line chart to show the trend of article length over time
fig_line = px.line(avg_article_length, 
                   x='Year-Month', 
                   y='length', 
                   title="Trend of Article Length Over Time", 
                   labels={'Year-Month': 'Year-Month', 'length': 'Average Article Length'},
                   markers=True)

# add annotations to emphasize trends or major events
# Code adapted with the help of chatgpt, check Solution GPT 1.4
fig_line.add_annotation(
    x='2022-06', 
    y=avg_article_length['length'].max(),
    text="Peak Article Length",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

fig_line.show()

# save the line chart to an HTML file
fig_line.write_html("../Visuals/Final_Visuals/Length_final_visuals/trend_article_length_over_time.html")

# plot a bar chart to show the average article length by Year-Month
fig_bar = px.bar(avg_article_length, 
                 x='Year-Month', 
                 y='length', 
                 title="Average Article Length by Year-Month", 
                 labels={'Year-Month': 'Year-Month', 'length': 'Average Article Length'},
                 color='length',  # Color the bars based on article length
                 color_continuous_scale='Plasma')  # Choosing a different color scale for distinction

# add annotations to highlight significant months or patterns
# Code adapted with the help of chatgpt, check Solution GPT 1.4
fig_bar.add_annotation(
    x='2022-12', 
    y=avg_article_length['length'].max(),
    text="End of year peak",
    showarrow=True,
    arrowhead=2,
    ax=0,
    ay=-40
)

fig_bar.show()

# save the bar chart to an HTML file
fig_bar.write_html("../Visuals/Final_Visuals/Length_final_visuals/avg_article_length_by_year_month.html")

