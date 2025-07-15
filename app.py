# Tennis Data Analytics Dashboard
# Import Libraries
import streamlit as st
import pandas as pd
import sqlite3
import altair as alt

# Set Page Configuration
st.set_page_config(page_title="Tennis Analytics", page_icon = ":tennis:", layout="wide")

# Apply CSS Styling
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Add title
st.title(":tennis: Tennis Data Analytics Dashboard")

# Connect to SQLite database
conn = sqlite3.connect("tennis_db.sqlite")

# Load Data 
competitors_df = pd.read_sql("SELECT * FROM competitors where country != 'Neutral'", conn)
rankings_df = pd.read_sql("SELECT * FROM competitor_rankings", conn)
competitions_df = pd.read_sql("SELECT * FROM competitions", conn)
categories_df = pd.read_sql("SELECT * FROM categories", conn)

# Merge for ease
merged_df = pd.merge(rankings_df, competitors_df, on="competitor_id", how="left")

# Sidebar Filters
st.sidebar.header("🔍 Filter Competitors")

# Filter widgets
name_filter = st.sidebar.selectbox("Select Competitor", ["All"] + sorted(merged_df["name"].dropna().unique().tolist()))
rank_range = st.sidebar.slider("Rank Range", int(merged_df["rank"].min()), int(merged_df["rank"].max()), (1, 100))
country_filter = st.sidebar.selectbox("Select Country", ["All"] + sorted(merged_df["country"].dropna().unique()))
points_threshold = st.sidebar.slider("Minimum Points", 0, int(merged_df["points"].max()), 0)

# KPI Cards
total_competitors = len(competitors_df)
total_countries = competitors_df["country"].nunique()
highest_points = rankings_df["points"].max()

col1, col2, col3 = st.columns(3)
col1.metric("Total Competitors", total_competitors, border = True)
col2.metric("Countries Represented", total_countries, border = True)
col3.metric("Highest Points", highest_points, border = True)

# Competitor Details Viewer
st.subheader("👤 Competitor Details")

if name_filter != "All":
    competitor_details = merged_df[merged_df["name"] == name_filter][[
        "name", "rank", "movement", "points", "competitions_played", "country"
    ]]
    st.table(competitor_details)
else:
    st.info("Please select a competitor from the sidebar")

# Country-wise Analysis
st.subheader("🌍 Country-wise Competitor Analysis")

country_analysis = merged_df.groupby("country").agg(
    num_competitors=pd.NamedAgg(column="competitor_id", aggfunc="count"),
    avg_points=pd.NamedAgg(column="points", aggfunc="mean")
).reset_index().sort_values(by="num_competitors", ascending=False)

st.dataframe(country_analysis)

# Create a bar chart for country-wise analysis
chart = alt.Chart(country_analysis.head(10)).mark_bar().encode(
    x=alt.X('country:N', title="Country"),
    y=alt.Y('num_competitors:Q', title="Number of Competitors"),
    tooltip=['country', 'num_competitors', 'avg_points']
).properties(title="Top 10 Countries by Number of Competitors")

# View chart
st.altair_chart(chart, use_container_width=True)

#  Leaderboards 
st.subheader("🏆 Leaderboards")

col1, col2 = st.columns(2)

with col1:
    top_ranked = merged_df.sort_values("rank").head(10)[
        ["name", "rank", "country", "points"]
    ]
    st.markdown("### Top Ranked Competitors")
    st.dataframe(top_ranked)

with col2:
    top_points = merged_df.sort_values("points", ascending=False).head(10)[
        ["name", "points", "country"]
    ]
    st.markdown("### Highest Point Scorers")
    st.dataframe(top_points)

# Filtered Table
st.subheader("📋 Filtered Competitors")

filtered_df = merged_df.copy()

if name_filter != "All":
    filtered_df = filtered_df[filtered_df["name"] == name_filter]
if country_filter != "All":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]

# Apply rank and points filters
filtered_df = filtered_df[
    (filtered_df["rank"] >= rank_range[0]) & 
    (filtered_df["rank"] <= rank_range[1]) & 
    (filtered_df["points"] >= points_threshold)
]

st.dataframe(filtered_df[["name", "rank", "movement", "points", "country"]])

# Close connection
conn.close()
