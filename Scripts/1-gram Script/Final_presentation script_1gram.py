"""This is the final presentation script with the help of Exploration script. Used slides and AI Documentation to build the exploration script and from that this one,
Full AI Documentation is mentioned in exploratiion part"""

# Import necessary Libraries
import pandas as pd
import plotly.express as px

# Load and Filter Data

# Load 1-gram data
df = pd.read_csv("../data/dataframes/n-grams/1-gram/1-gram.csv")

# Convert year, month, day to datetime
df["date"] = pd.to_datetime(df[["year", "month", "day"]])

# Keep only rows from May 2021 onwards
df = df[df["date"] >= "2021-05-01"]

# Define Word Categories

# Define conflict and peace words
conflict_words = ['war', 'attacks', 'attack', 'children', 'ground', 'palestinians', 'military', 'forces', 'besieged', 'hamas', 'civilians']
peace_words = ['united', 'nations', 'international', 'well', 'end']

# Function to assign category
# code adapted with the help of Chatgpt, check solution 1.2
def label_category(word):
    if word in conflict_words:
        return "conflict"
    elif word in peace_words:
        return "peace"
    else:
        return None

# Apply category to each row
# code adapted with the help of Chatgpt, check solution 1.2
df["category"] = df["1-gram"].apply(label_category)


# 1. Bar Chart - Total Frequency (Yearly)


# Extract year from date
df["year"] = df["date"].dt.year

# Group by year and category, sum counts
# coded adapted from slides 14.1
# Also, Chatgpt, check solution 1.3
grouped_year = df[df["category"].notna()].groupby(["year", "category"])["count"].sum().reset_index()

# Plot bar chart (total frequency - yearly)
# Code adapted from slide 15.1
fig1 = px.bar(
    grouped_year,
    x="year",
    y="count",
    color="category",
    barmode="group",
    title="Total Frequency of Conflict and Peace Words (Yearly)",
    text="count"
)
# save the output as HTML file
fig1.write_html("../Visuals/Final_Visuals/1-gram_Visuals/bar_total_yearly.html")
fig1.show()


# 2. Bar Chart - Total Frequency (Monthly)


# Extract month (like '2022-04')
# code adapted with the help of chatgpt check solution 1.2

df["month_str"] = df["date"].dt.to_period("M").astype(str)

# Group by month and category
# coded adapted from slides 14.1
# Also, Chatgpt, check solution 1.3, there is a small change from the previous code, change year to month
grouped_month = df[df["category"].notna()].groupby(["month_str", "category"])["count"].sum().reset_index()

# Plot bar chart (total frequency - monthly)
# code adpated from Slides 15.1
fig2 = px.bar(
    grouped_month,
    x="month_str",
    y="count",
    color="category",
    barmode="group",
    title="Total Frequency of Conflict and Peace Words (Monthly)",
    text="count"
)
fig2.update_layout(xaxis_tickangle=-45)

# save the output as HTML file
fig2.write_html("../Visuals/Final_Visuals/1-gram_Visuals/bar_total_monthly.html")
fig2.show()

# 3. Bar Chart - Relative Frequency (Yearly)

# Total 1-gram counts per year
# code adapted with the help of slide 14.1
# Also, code adapted with the help of Chatgpt, check solution 1.4
total_per_year = df.groupby("year")["count"].sum().reset_index().rename(columns={"count": "total_count"})

# Conflict/peace counts per year
# code adapted with the help of Chatgpt, check solution 1.3
grouped_year_rel = df[df["category"].notna()].groupby(["year", "category"])["count"].sum().reset_index()

# Merge to compute relative frequency
# Check Solution 1.7
grouped_year_rel = grouped_year_rel.merge(total_per_year, on="year")
grouped_year_rel["relative_freq"] = grouped_year_rel["count"] / grouped_year_rel["total_count"]

# Plot bar chart (relative frequency - yearly)
fig3 = px.bar(
    grouped_year_rel,
    x="year",
    y="relative_freq",
    color="category",
    barmode="group",
    title="Relative Frequency of Conflict and Peace Words (Yearly)",
    text="relative_freq"
)
fig3.write_html("../Visuals/Final_Visuals/1-gram_Visuals/bar_relative_yearly.html")
fig3.show()

# 4. Bar Chart - Relative Frequency (Monthly)


# Total 1-gram counts per month
total_per_month = df.groupby("month_str")["count"].sum().reset_index().rename(columns={"count": "total_count"})

# Conflict/peace counts per month
grouped_month_rel = df[df["category"].notna()].groupby(["month_str", "category"])["count"].sum().reset_index()

# Merge and calculate relative frequency
grouped_month_rel = grouped_month_rel.merge(total_per_month, on="month_str")
grouped_month_rel["relative_freq"] = grouped_month_rel["count"] / grouped_month_rel["total_count"]

# Plot bar chart (relative frequency - monthly)
# codes adapted from slides 15.1
fig4 = px.bar(
    grouped_month_rel,
    x="month_str",
    y="relative_freq",
    color="category",
    barmode="group",
    title="Relative Frequency of Conflict and Peace Words (Monthly)",
    text="relative_freq"
)
fig4.update_layout(xaxis_tickangle=-45)
# save the Output as HTML file
fig4.write_html("../Visuals/Final_Visuals/1-gram_Visuals/bar_relative_monthly.html")
fig4.show()
