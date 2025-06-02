# import necessary libraries

import pandas as  pd
import plotly.express as px


# load the dataframe
df = pd.read_csv("../length/length-year-month.csv")
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
