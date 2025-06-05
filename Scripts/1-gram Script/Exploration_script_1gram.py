"""The following Whole script is exploration script, I used many things, used many methods, after using this script, i will make a final script"""


#------------------------------------------------------|
# This first of set of code is find most frequent words|
#------------------------------------------------------|

import pandas as pd
import plotly.express as px

# Load the merged dataset
df = df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Preprocess the '1-gram' column to remove stop words
# List of common stop words (you've already provided the stop words list)
stop_words = [
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", 
    "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", 
    "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", 
    "theirs", "themselves", "what", "which", "who", "whom", "this", "that", 
    "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", 
    "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", 
    "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", 
    "at", "by", "for", "with", "about", "against", "between", "into", "through", 
    "during", "before", "after", "above", "below", "to", "from", "up", "down", 
    "in", "out", "on", "off", "over", "under", "again", "further", "then", 
    "once", "here", "there", "when", "where", "why", "how", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
    "not", "only", "own", "same", "so", "than", "too", "very", "can", "will", 
    "just", "don", "should", "now", "15", "s", "said" , "one", "would", "told",
    "also", "since", "two", "al", "also", "including", "day", "days", "could", "according", "among", "weeks", "made", "ground", "least", "time"
    "october", "strip", "november", "october", "southern", "air", "benjamin", "month", "part", "thousands",
    "time", "called", "come", "added", "even", "last", "world", "jazeera",
    "many", "take", "group", "amid", "group", "several", "enclave"
]

# Clean the '1-gram' column
# code adapted with help of chatgpt, check Solution 1.1
df['1-gram'] = df['1-gram'].astype(str)  # Ensure all values are strings
df['1-gram'] = df['1-gram'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))  # Remove stop words

# Remove unwanted 1-grams (e.g., empty strings and numerical 1-grams)
df_cleaned = df[~df['1-gram'].str.match(r'^\d+$')]  # Remove 1-grams that are numbers only
df_cleaned = df_cleaned[df_cleaned['1-gram'] != '']  # Remove empty strings

# Calculate the top 20 most frequent 1-grams
top_20_1grams = df_cleaned['1-gram'].value_counts().head(20)

print(top_20_1grams)

#  Create a bar chart of the top 20 frequent 1-grams
fig = px.bar(top_20_1grams, 
             x=top_20_1grams.index, 
             y=top_20_1grams.values, 
             labels={'x': '1-gram', 'y': 'Frequency'},
             title='Top 20 Most Frequent 1-grams (Cleaned)')

# Show the plot
fig.show()
#-----------------------------------------------------------------------------------------------------------------------------------------------------|
# this second set of code is to group the words taken from most frequent words and Plot a line chart of most frquent words by year and month separetly|
#-----------------------------------------------------------------------------------------------------------------------------------------------------|

#import neccessary libraries
import pandas as pd
import plotly.express as px

# read the 1-gram CSV file into a DataFrame
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Combine year, month, day into a datetime column
# create a single 'date' column by combining 'year', 'month', and 'day' columns
# code adapted from Slides 14.1
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Define your conflict and peace word groups
# define lists of words associated with conflict and peace
conflict_words = ['war', 'attacks', 'attack', 'children', 'ground', 'palestinians', 'military', 'forces', 'besieged', 'hamas', 'civilians']
peace_words = ['united', 'nations', 'international', 'well', 'end']

# Categorize each word
# function to label each word as 'conflict', 'peace', or None
# code adapted with the help of Chatgpt, check solution 1.2
def label_category(word):
    if word in conflict_words:
        return "conflict"
    elif word in peace_words:
        return "peace"
    else:
        return None

# apply the labeling function to each word in the '1-gram' column
# code adapted with the help of Chatgpt, check solution 1.2
df["category"] = df["1-gram"].apply(label_category)

# Extract year and group counts
# extract year from the 'date' column
# code adapted with the help of Chatgpt, check solution 1.2
df["year"] = df["date"].dt.year

# filter only rows that belong to either conflict or peace category
# code adapted with the help of Chatgpt, check solution 1.3
filtered_df = df[df["category"].insull()]                                                     

# group the filtered rows by year and category and sum the count column
# coded adapted from slides 14.1
grouped = filtered_df.groupby(["year", "category"])["count"].sum().reset_index()

#  Manually create separate columns for conflict and peace counts
# create a dataframe for conflict word counts per year
# code adapted with the help of Chatgpt, check solution 1.4
conflict_df = grouped[grouped["category"] == "conflict"][["year", "count"]].rename(columns={"count": "conflict"})

# create a dataframe for peace word counts per year
# code adapted with the help of Chatgpt, check solution 1.4
peace_df = grouped[grouped["category"] == "peace"][["year", "count"]].rename(columns={"count": "peace"})

# merge both conflict and peace dataframes on year
# code adapted with the help of Chatgpt, check solution 1.5
merged_df = pd.merge(conflict_df, peace_df, on="year", how="outer").fillna(0)                                                 

# calculate the difference column (conflict - peace)
merged_df["difference"] = merged_df["conflict"] - merged_df["peace"]

# Plot the trend
# create a line plot showing conflict, peace, and difference over the years
# Code adapted from slide 15.1
fig = px.line(
    merged_df,
    x="year",
    y=["conflict", "peace", "difference"],
    title="Conflict vs Peace Language in Al Jazeera Gaza Corpus (Yearly)",
    labels={"value": "Word Count", "year": "Year", "variable": "Category"},
    markers=True
)
fig.show()

# this is for monthly frequency count for line chart

# create a month column in the format YYYY-MM
# code adapted with the help of chatgpt check solution 1.2
df["month"] = df["date"].dt.to_period("M").astype(str)                

# filter again for rows with a valid category
# code adapted with the help of Chatgpt, check solution 1.3
filtered_df = df[df["category"].insull()]                          

# group by month and category and sum counts
# code adapted from slide 14.1 
grouped_monthly = filtered_df.groupby(["month", "category"])["count"].sum().reset_index()

# create separate dataframes for conflict and peace word counts per month
# code adapted with the help of Chatgpt, check solution 1.4, it was for year this is for month, so here there is small change
conflict_monthly = grouped_monthly[grouped_monthly["category"] == "conflict"][["month", "count"]].rename(columns={"count": "conflict"})
peace_monthly = grouped_monthly[grouped_monthly["category"] == "peace"][["month", "count"]].rename(columns={"count": "peace"})

# merge conflict and peace dataframes on month
# code adapted with the help of Chatgpt, check solution 1.5
merged_monthly = pd.merge(conflict_monthly, peace_monthly, on="month", how="outer").fillna(0)         ]

# calculate the difference for each month
merged_monthly["difference"] = merged_monthly["conflict"] - merged_monthly["peace"]

# plot monthly trends
# code adapted from slide 15.1
fig = px.line(
    merged_monthly,
    x="month",
    y=["conflict", "peace", "difference"],
    title="Conflict vs Peace Language in Al Jazeera Gaza Corpus (Monthly)",
    labels={"value": "Word Count", "month": "Month", "variable": "Category"},
    markers=True
)
fig.show()

#------------------------------------------------------------------------------------------------|
# this Third set of code is to Plot a bar chart of most frquent words by year and month separetly|
#------------------------------------------------------------------------------------------------|

import pandas as pd
import plotly.express as px

# Load data
# read the 1-gram CSV file into a DataFrame
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Combine into a datetime column
# create a single 'date' column from year, month, and day
# code adapted from Slides 14.1
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Define word groups
# list of conflict-related and peace-related words
conflict_words = ['war', 'attacks', 'attack', 'children', 'ground', 'palestinians', 'military', 'forces', 'besieged', 'hamas', 'civilians']
peace_words = ['united', 'nations', 'international', 'well', 'end']

# Categorize each word
# function to assign 'conflict', 'peace', or None to each word
# code adapted with the help of Chatgpt, check solution 1.2
def label_category(word):
    if word in conflict_words:
        return "conflict"
    elif word in peace_words:
        return "peace"
    else:
        return None

# apply the function to the 1-gram column
# code adapted with the help of Chatgpt, check solution 1.2
df["category"] = df["1-gram"].apply(label_category)

# Yearly Aggregation
# extract year from date
# code adapted with the help of Chatgpt, check solution 1.2
df["year"] = df["date"].dt.year

# filter only rows with a category and group by year and category
# code adapted with the help of slide 14.1
grouped_year = (
    df[df["category"].notna()]                                           
    .groupby(["year", "category"])["count"]
    .sum()
    .reset_index()
)

# separate conflict and peace word counts into two DataFrames
# code adapted with the help of Chatgpt, check solution 1.4
conflict_year = grouped_year[grouped_year["category"] == "conflict"][["year", "count"]].rename(columns={"count": "conflict"})
peace_year = grouped_year[grouped_year["category"] == "peace"][["year", "count"]].rename(columns={"count": "peace"})

# merge both on year and fill missing values with 0
# code adapted with the help of Chatgpt, check solution 1.5
merged_year = pd.merge(conflict_year, peace_year, on="year", how="outer").fillna(0)

# calculate difference column (conflict - peace)
merged_year["difference"] = merged_year["conflict"] - merged_year["peace"]

# prepare data manually for bar chart (one row per year per category)
# code adapted with the help of Chatgpt, check solution 1.6
year_conflict = merged_year[["year", "conflict"]].copy()
year_conflict["Category"] = "conflict"
year_conflict = year_conflict.rename(columns={"conflict": "Word Count"})

year_peace = merged_year[["year", "peace"]].copy() 
year_peace["Category"] = "peace"
year_peace = year_peace.rename(columns={"peace": "Word Count"})

year_difference = merged_year[["year", "difference"]].copy()
year_difference["Category"] = "difference"
year_difference = year_difference.rename(columns={"difference": "Word Count"})

# combine all three into one DataFrame for plotting
# code adapted with the help of Chatgpt, check solution 1.6
plot_year = pd.concat([year_conflict, year_peace, year_difference], ignore_index=True)                    

# Bar Chart - Yearly
# create a grouped bar chart for yearly comparison
# code adapted from Slides 15.1
fig = px.bar(
    plot_year,
    x="year",
    y="Word Count",
    color="Category",
    barmode="group",
    title="Conflict vs Peace Language in Al Jazeera Gaza Corpus (Yearly)",
    text="Word Count"
)
fig.show()

# Monthly Aggregation
# extract month in format YYYY-MM
# code adapted with the help of Chatgpt, check solution 1.2
df["month"] = df["date"].dt.to_period("M").astype(str)                

# group by month and category and sum counts
# code adapted from slides
# code adapted with the help of Slides 14.1
grouped_month = (
    df[df["category"].notna()]
    .groupby(["month", "category"])["count"]
    .sum()
    .reset_index()
)

# split into conflict and peace word monthly counts
conflict_month = grouped_month[grouped_month["category"] == "conflict"][["month", "count"]].rename(columns={"count": "conflict"})
peace_month = grouped_month[grouped_month["category"] == "peace"][["month", "count"]].rename(columns={"count": "peace"})

# merge on month and fill NaNs with 0
# code adapted with the help of Chatgpt, check solution 1.5
merged_month = pd.merge(conflict_month, peace_month, on="month", how="outer").fillna(0)               

# calculate difference
merged_month["difference"] = merged_month["conflict"] - merged_month["peace"]

# prepare data manually for monthly bar chart
# code adapted with the help of Chatgpt, check solution 1.6
month_conflict = merged_month[["month", "conflict"]].copy()
month_conflict["Category"] = "conflict"
month_conflict = month_conflict.rename(columns={"conflict": "Word Count"})

month_peace = merged_month[["month", "peace"]].copy()
month_peace["Category"] = "peace"
month_peace = month_peace.rename(columns={"peace": "Word Count"})

month_difference = merged_month[["month", "difference"]].copy()
month_difference["Category"] = "difference"
month_difference = month_difference.rename(columns={"difference": "Word Count"})

# combine for plotting
# code adapted with the help of Chatgpt, check solution 1.6
plot_month = pd.concat([month_conflict, month_peace, month_difference], ignore_index=True)                          

# Bar Chart - Monthly
# plot monthly grouped bar chart with rotated x-axis
# coded adapted from Slides 15.1
fig = px.bar(
    plot_month,
    x="month",
    y="Word Count",
    color="Category",
    barmode="group",
    title="Conflict vs Peace Language in Al Jazeera Gaza Corpus (Monthly)",
    text="Word Count"
)
fig.update_layout(xaxis_tickangle=-45)
fig.show()

#---------------------------------------------------------------------------------------------------|
#This Fourth set of code is to find relative frequecncy through bar chart through yearly and monthly|
#---------------------------------------------------------------------------------------------------|

"""For the following most of the copied from above, any documentation to new codes will be there"""

# import necessary libraries
import pandas as pd
import plotly.express as px

# Load the 1-gram CSV file into a DataFrame
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Combine year, month, and day columns into a single datetime column
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Define conflict and peace word lists
conflict_words = ['war', 'attacks', 'attack', 'children', 'ground', 'palestinians', 'military', 'forces', 'besieged', 'hamas', 'civilians']
peace_words = ['united', 'nations', 'international', 'well', 'end']

# Function to assign category based on word
def label_category(word):
    if word in conflict_words:
        return "conflict"
    elif word in peace_words:
        return "peace"
    else:
        return None

# Apply the label_category function to the '1-gram' column to create a 'category' column
df["category"] = df["1-gram"].apply(label_category)

# YEARLY RELATIVE FREQUENCY 

# Extract year from date
df["year"] = df["date"].dt.year

# Calculate total word count per year
total_per_year = df.groupby("year")["count"].sum().reset_index().rename(columns={"count": "total_count"})

# Calculate total conflict word counts per year
conflict_per_year = df[df["category"] == "conflict"].groupby("year")["count"].sum().reset_index().rename(columns={"count": "conflict"})

# Calculate total peace word counts per year
peace_per_year = df[df["category"] == "peace"].groupby("year")["count"].sum().reset_index().rename(columns={"count": "peace"})

# Merge all yearly counts into one DataFrame
merged_year = total_per_year.merge(conflict_per_year, on="year", how="left").merge(peace_per_year, on="year", how="left")

# Replace NaN with 0 for years where category was missing
merged_year[["conflict", "peace"]] = merged_year[["conflict", "peace"]].fillna(0)

# Calculate relative frequency for conflict and peace
# code adapted with the help of Chatgpt, check solution 1.8 
merged_year["conflict_rel"] = merged_year["conflict"] / merged_year["total_count"]
merged_year["peace_rel"] = merged_year["peace"] / merged_year["total_count"]

# Calculate difference in relative frequency
merged_year["difference"] = merged_year["conflict_rel"] - merged_year["peace_rel"]

# Prepare data for plotting
# code adapted with the help of Chatgpt, check solution 1.7
year_plot_data = pd.DataFrame({
    "year": pd.concat([merged_year["year"]]*3, ignore_index=True),                   
    "Category": ["conflict"]*len(merged_year) + ["peace"]*len(merged_year) + ["difference"]*len(merged_year),
    "Relative Frequency": pd.concat([merged_year["conflict_rel"], merged_year["peace_rel"], merged_year["difference"]], ignore_index=True)
})

# Plot yearly bar chart
# code adapted from Slides 15.1 
fig_yearly = px.bar(
    year_plot_data,
    x="year",
    y="Relative Frequency",
    color="Category",
    barmode="group",
    title="Relative Frequency of Conflict vs Peace Words (Yearly)",
    text="Relative Frequency"
)
fig_yearly.show()

#MONTHLY RELATIVE FREQUENCY

""" the follwoing code is directly with some so no documentation needed for this specific part"""

# Extract month in 'YYYY-MM' format
df["month"] = df["date"].dt.to_period("M").astype(str)

# Calculate total word count per month
total_per_month = df.groupby("month")["count"].sum().reset_index().rename(columns={"count": "total_count"})

# Calculate total conflict word counts per month
conflict_per_month = df[df["category"] == "conflict"].groupby("month")["count"].sum().reset_index().rename(columns={"count": "conflict"})

# Calculate total peace word counts per month
peace_per_month = df[df["category"] == "peace"].groupby("month")["count"].sum().reset_index().rename(columns={"count": "peace"})

# Merge all monthly counts into one DataFrame
merged_month = total_per_month.merge(conflict_per_month, on="month", how="left").merge(peace_per_month, on="month", how="left")

# Replace NaN with 0 for months where category was missing
merged_month[["conflict", "peace"]] = merged_month[["conflict", "peace"]].fillna(0)     

# Calculate relative frequency for conflict and peace
merged_month["conflict_rel"] = merged_month["conflict"] / merged_month["total_count"]
merged_month["peace_rel"] = merged_month["peace"] / merged_month["total_count"]

# Calculate difference in relative frequency
merged_month["difference"] = merged_month["conflict_rel"] - merged_month["peace_rel"]

# Prepare data for plotting (manual melt)
month_plot_data = pd.DataFrame({
    "month": pd.concat([merged_month["month"]]*3, ignore_index=True),               
    "Category": ["conflict"]*len(merged_month) + ["peace"]*len(merged_month) + ["difference"]*len(merged_month),
    "Relative Frequency": pd.concat([merged_month["conflict_rel"], merged_month["peace_rel"], merged_month["difference"]], ignore_index=True)       #chatgpt
})

# Plot monthly bar chart
fig_monthly = px.bar(
    month_plot_data,
    x="month",
    y="Relative Frequency",
    color="Category",
    barmode="group",
    title="Relative Frequency of Conflict vs Peace Words (Monthly)",
    text="Relative Frequency"
)
fig_monthly.update_xaxes(type='category')  # Keeps months in order
fig_monthly.show()






