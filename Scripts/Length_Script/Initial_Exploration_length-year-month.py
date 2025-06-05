# import necessary libraries

import pandas as  pd
import plotly.express as px


# load the dataframe
df = pd.read_csv("../data/dataframes/length/length-year-month.csv")
print(df)

# show first few rows
print("First 5 rows of the data:")
print(df.columns)
print(df.head())

# check for number of rows and columns
print("\nShape of the dataset (rows, columns):")
print(df.shape)

# check unique years and month
print("\nUnique years:")
print(df['year'].unique())
print("\nUnique months:")
print(df['month'].unique())

# sort by year and month to make a easier analysis
df = df.sort_values(by=['year', 'month'])
print(df)

#Remove row year 2017, because there is only one row with year 2017, so it is insignificnat
df = df[df['year'] != 2017]

# After removing row reset the index
df = df.reset_index(drop=True)
print(df)

print("n\final dataset shape")
print(df.shape)

# create a new data column
# this combines year and month into a real date. Set day to 1
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

# show dataframe
print(df)

# VISUALIZATION 1: Total Coverage Over Time (line Plot)
fig1 = px.line(
    df,       # our dataframe
    x='date', # x-axis is the timeline
    y='length-sum', # y-axis is the total article length
    title='Total Media Coverage Over Time (length-sum)',
    labels={'date': 'Date', 'length-mean': 'Average Length'}
    )

# save the ouput as HTML and PNG file
fig1.write_html("../Visuals/Test_Visuals/fig1_total_coverage.html")
fig1.write_image("../Visuals/Test_Visuals/fig1_total_coverage.png")

# show plot
fig1.show()

# VISUALIZATION 2: Average Article Length Over Time
fig2 = px.line(
    df,  # our dataframe
    x='date',  # x-axis is time
    y='length-mean',  # y-axis is average length
    title='Average Article Length Over Time (length-mean)',
    labels={'date': 'Date', 'length-mean': 'Average Length'}
)

# save the ouput as HTML and PNG file
fig2.write_html("../Visuals/Test_Visuals/fig2_average_length.html")
fig2.write_image("../Visuals/Test_Visuals/fig2_average_length.png")

#show plot
fig2.show()

# VISUALIZATION 3: Top 5 Months by Total Article Length
# make a copy so, it will not effect the original dataframe.
df_top = df.copy()

# to find highest coverage, sort by 'length-sum'
df_top_sorted = df_top.sort_values(by='length-sum', ascending=False)

# select the top 5 months
df_top5 = df_top_sorted.head(5)

# make a bar chart
fig3 = px.bar(
    df_top5,
    x='date',
    y='length-sum',
    title='Top 5 Months by Total Article Length',
    labels={'date': 'Month', 'length-sum': 'Total Article Length (Words)'},
    color='length-sum',
    color_continuous_scale='reds'
)

# save the  ouput as HTML and PNG
fig3.write_html("../Visuals/Test_Visuals/fig3_Top5_months.html")
fig3.write_image("../Visuals/Test_Visuals/fig3_Top5_months.png")

#show bar chart
fig3.show()


"""I explored this length-year-month dataframe, and I am unable to formulate an argument for year-month dataframe, so choose length data frame to work"""



