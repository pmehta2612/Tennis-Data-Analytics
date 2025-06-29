import streamlit as st
import pandas as pd
import plotly.express as px
from utils import run_query

st.set_page_config(layout="wide", page_title="Tennis Data Dashboard")

# Sidebar Filters
st.sidebar.header("🎾 Competitor Filters")

# Fetch all filter data
competitor_names = run_query("SELECT DISTINCT name FROM competitors ORDER BY name")['name']
countries = run_query("SELECT DISTINCT country FROM competitors ORDER BY country")['country']
competition_types = run_query("SELECT DISTINCT type FROM competitions")['type']
categories = run_query("SELECT DISTINCT category_name FROM categories")['category_name']

# Filters
selected_name = st.sidebar.selectbox("Search by Name", options=["All"] + list(competitor_names))
rank_range = st.sidebar.slider("Filter by Rank", 1, 1000, (1, 1000))
points_threshold = st.sidebar.slider("Min Points", 0, 10000, 0)
selected_country = st.sidebar.selectbox("Filter by Country", ["All"] + list(countries))
selected_type = st.sidebar.selectbox("Competition Type", ["All"] + list(competition_types))
selected_category = st.sidebar.selectbox("Category", ["All"] + list(categories))

# ---- HOME DASHBOARD ----
st.title("🏆 Tennis Analytics Dashboard")

col1, col2, col3 = st.columns(3)
total_competitors = run_query("SELECT COUNT(*) as count FROM competitors")['count'].iloc[0]
total_countries = run_query("SELECT COUNT(DISTINCT country) as count FROM competitors")['count'].iloc[0]
max_points = run_query("SELECT MAX(points) as max_points FROM competitor_rankings")['max_points'].iloc[0]

col1.metric("Total Competitors", total_competitors)
col2.metric("Countries Represented", total_countries)
col3.metric("Highest Points", max_points)

st.markdown("---")

# ---- COMPETITOR DETAILS VIEWER ----
st.header("👤 Competitor Detail Viewer")
if selected_name != "All":
    details_query = """
    SELECT c.name, c.country, r.rank, r.movement, r.competitions_played, r.points
    FROM competitors c
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
    WHERE c.name = %s
    """
    competitor_details = run_query(details_query, params=(selected_name,))
    st.table(competitor_details)
else:
    st.info("Please select a competitor from the sidebar.")

# ---- FILTERED COMPETITORS LIST ----
st.header("🔎 Filtered Competitors List")

filter_query = """
SELECT c.name, c.country, r.rank, r.points, r.movement
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
WHERE r.rank BETWEEN %s AND %s
AND r.points >= %s
""" + (" AND c.country = %s" if selected_country != "All" else "") + ";"

params = (rank_range[0], rank_range[1], points_threshold)
if selected_country != "All":
    params += (selected_country,)

competitors_filtered = run_query(filter_query, params)
st.dataframe(competitors_filtered)

# ---- COUNTRY-WISE ANALYSIS ----
st.header("🌍 Country-Wise Analysis")

country_stats = run_query("""
SELECT c.country, COUNT(*) AS total_competitors, AVG(r.points) AS avg_points
FROM competitors c
JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
GROUP BY c.country
ORDER BY total_competitors DESC
""")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Bar Chart: Competitors by Country")
    st.plotly_chart(px.bar(country_stats, x="country", y="total_competitors"))

with col2:
    st.subheader("Bar Chart: Avg Points by Country")
    st.plotly_chart(px.bar(country_stats, x="country", y="avg_points"))

# Display SQL table
st.subheader("📋 Country Stats Table")
st.dataframe(country_stats)

# ---- LEADERBOARDS ----
st.header("🏅 Leaderboards")

col1, col2 = st.columns(2)

with col1:
    top_ranked = run_query("""
    SELECT c.name, c.country, r.rank, r.points
    FROM competitors c
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.rank ASC
    LIMIT 10
    """)
    st.subheader("Top Ranked Competitors")
    st.dataframe(top_ranked)

with col2:
    top_points = run_query("""
    SELECT c.name, c.country, r.points
    FROM competitors c
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
    ORDER BY r.points DESC
    LIMIT 10
    """)
    st.subheader("Top Point Scorers")
    st.dataframe(top_points)

st.markdown("---")

