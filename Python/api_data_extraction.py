
# **API Data Extraction**
# Importing Libraries
import requests
import pandas as pd
from pandas import json_normalize

# 1. Extracting Competitions data from API Endpoint
url = "https://api.sportradar.com/tennis/trial/v3/en/competitions.json"

headers = {
    "accept": "application/json",
    "x-api-key": "wDF634G92J7N9MH1karTymHlTMgjUoy7XUB4Vvze"
}

response = requests.get(url, headers=headers)
raw_json = response.json()

print(raw_json)

# 2. Extracting Complexes data from API Endpoint
url = "https://api.sportradar.com/tennis/trial/v3/en/complexes.json"

headers = {
    "accept": "application/json",
    "x-api-key": "wDF634G92J7N9MH1karTymHlTMgjUoy7XUB4Vvze"
}

response = requests.get(url, headers=headers)
raw_json1 = response.json()

print(raw_json1)

# 3. Extracting Double Competitor Rankings data from API Endpoint

url = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

headers = {
    "accept": "application/json",
    "x-api-key": "wDF634G92J7N9MH1karTymHlTMgjUoy7XUB4Vvze"
}

response = requests.get(url, headers=headers)
raw_json2 = response.json()

print(raw_json2)

"""## **Normalizing into Tables**

### 1. **Competitions API**
"""

# 1. Categories Table
# Flatten the category object that sits inside every competition record ---
categories_df = (
    json_normalize(
        raw_json["competitions"],           # list of competitions
        record_path=None,                   # we don’t want to explode anything
        meta=[["category", "id"], ["category", "name"]],
        errors="ignore"
    )
    .rename(columns={
        "category.id": "category_id",
        "category.name": "category_name"
    })
    [["category_id", "category_name"]]     # keep only the two columns we need
    .drop_duplicates()
    .reset_index(drop=True)
)

# View data
print(categories_df.head())

# 2. Competitions Table
# Flatten each competition, keeping the category ID for the FK
competitions_df = (
    json_normalize(raw_json["competitions"])
    .rename(columns={
        "id": "competition_id",
        "name": "competition_name",
        "category.id": "category_id"
    })
    [["competition_id", "competition_name",
      "parent_id", "type", "gender", "category_id"]]
    .astype({"parent_id": "string"})       # ensure consistent dtypes (optional)
    .reset_index(drop=True)
)

# View Data
print(competitions_df.head())

"""### 2. **Complexes API**"""

# Get list of complexes from API response (empty list if missing)
complexes_list = raw_json1.get("complexes", [])

# 1. Complexes Table
complexes_df = (
    pd.json_normalize(complexes_list)
      .rename(columns={"id": "complex_id", "name": "complex_name"})
      [["complex_id", "complex_name"]]
      .drop_duplicates()
      .reset_index(drop=True)
)
# View data
print(complexes_df.head())

# Gather rows in a list first
venue_rows = []

# 2. Venues Table
for comp in complexes_list:
    for v in comp.get("venues", []):              # safely skip complexes with no venues
        venue_rows.append({
            "venue_id":     v.get("id"),
            "venue_name":   v.get("name"),
            "city_name":    v.get("city_name"),
            "country_name": v.get("country_name"),
            "country_code": v.get("country_code"),
            "timezone":     v.get("timezone"),
            "complex_id":   comp.get("id")        # FK back to Complexes
        })


# View data
print(venue_rows)

"""### 3. **Double Competitor Rankings API**"""

# 1.Competitor_Rankings Table

# Loop through each rankings block and pull the rows
rows = []

for block in raw_json2.get("rankings", []):                # e.g., ATP-men-week-26
    for r in block.get("competitor_rankings", []):        # the list of players
        rows.append({
            "rank"               : r.get("rank"),
            "movement"           : r.get("movement"),
            "points"             : r.get("points"),
            "competitions_played": r.get("competitions_played"),
            "competitor_id"      : r.get("competitor", {}).get("id")
        })

print(rows)

# 2. Competitors Table

# Gather competitor details into a list of dictionaries
comp_rows = []

for block in raw_json2.get("rankings", []):
    for r in block.get("competitor_rankings", []):
        c = r.get("competitor", {})
        comp_rows.append({
            "competitor_id": c.get("id"),
            "name":          c.get("name"),
            "country":       c.get("country"),
            "country_code":  c.get("country_code"),
            "abbreviation":  c.get("abbreviation")
        })
print(comp_rows)

"""## **Convert all Normalize Tables to Pandas DataFrame**

#### 1. **Competitions**
"""

# 1. Categories Table
categories_df = pd.DataFrame(categories_df)
print(f"Number of Rows = {categories_df.shape[0]}\nNumber of Columns = {categories_df.shape[1]}")
categories_df.head()

# 2. Competitions Table
competitions_df = pd.DataFrame(competitions_df)
print(f"Number of Rows = {competitions_df.shape[0]}\nNumber of Columns = {competitions_df.shape[1]}")
competitions_df.head()

"""#### 2. **Complexes**"""

# 1. Complexes Table
complexes_df = pd.DataFrame(complexes_df)
print(f"Number of Rows = {complexes_df.shape[0]}\nNumber of Columns = {complexes_df.shape[1]}")
complexes_df.head()

# 2. Venue Table
venue_df = pd.DataFrame(venue_rows)
print(f"Number of Rows = {venue_df.shape[0]}\nNumber of Columns = {venue_df.shape[1]}")
venue_df.head()

"""#### **3. Double Competitor Ranking**"""

# 1. Competitor Rankings Table

competitor_rankings_df = pd.DataFrame(rows)

# Add rank_id as an auto-increment surrogate key
competitor_rankings_df.insert(
    0,                                 # position for new column
    "rank_id",
    range(1, len(competitor_rankings_df) + 1)
)

# Keep columns in the required order
competitor_rankings_df = competitor_rankings_df[
    ["rank_id", "rank", "movement", "points",
     "competitions_played", "competitor_id"]
]

# View data
print(f"Number of Rows = {competitor_rankings_df.shape[0]}\nNumber of Columns = {competitor_rankings_df.shape[1]}")
competitor_rankings_df.head()

# 2. Competitors Table
# Build the DataFrame and keep one row per competitor
competitors_df = (
    pd.DataFrame(comp_rows)
      .drop_duplicates(subset=["competitor_id"])   # remove duplicates
      .reset_index(drop=True)
      [["competitor_id", "name", "country", "country_code", "abbreviation"]]
)

# View data
print(f"Number of Rows = {competitors_df.shape[0]}\nNumber of Columns = {competitors_df.shape[1]}")
competitors_df.head()

"""## **Data Wrangling**

## **Competitions API**
### **1.Categories Table**
"""

# Create copy of dataset
df_categories = categories_df.copy()

# View dataset
df_categories.head()

# Dataset information
df_categories.info()

# Check null values
df_categories.isnull().sum()

# Describe dataset
df_categories.describe()

"""### **2.Competitions Table**"""

# Create copy of dataset
df_competitions = competitions_df.copy()

# View dataset
df_competitions.head()

# Dataset Info
df_competitions.info()

# Describe dataset
df_competitions.describe()

# Check null values
df_competitions.isnull().sum()

df_competitions.head()

"""## **Complexes API**
### **1.Complexes Table**
"""

# Create copy of dataset
df_complexes = complexes_df.copy()

# View dataset
df_complexes.head()

# Dataset Info
df_complexes.info()

# Describe Dataset
df_complexes.describe()

"""### **Venue Table**"""

# Create copy of dataset
df_venue = venue_df.copy()

# View dataset
df_venue.head()

# Dataset Info
df_venue.info()

# Describe dataset
df_venue.describe()

# Check null values
print("Null values in dataset =",df_venue.isnull().sum().sum())

# Standardize values in proper case for venue name column
df_venue['venue_name'] = df_venue['venue_name'].str.title()

# View cleaned dataset
df_venue.head()

"""## **Double Competitor Ranking API**
### **1.Competitor Rankings Table**
"""

# Create copy of dataset
df_competitor_rankings = competitor_rankings_df.copy()

# View dataset
df_competitor_rankings.head()

# Dataset Info
df_competitor_rankings.info()

# Describe dataset
df_competitor_rankings.describe()

# Check null values
print("Null values in dataset =",df_competitor_rankings.isnull().sum().sum())

"""### **2.Competitor Table**"""

# Create copy of dataset
df_competitors = competitors_df.copy()

# View dataset
df_competitors.head()

# Dataset Info
df_competitors.info()

# Describe dataset
df_competitors.describe()

# Check missing values
df_competitors.isnull().sum()

"""## **Merge All Datasets**"""

# Merging All Datasets
# 1. Merge Competitions with Categories
competitions_merged = df_competitions.merge(
    df_categories,
    on="category_id",
    how="left"
)

# 2. Merge Venues with Complexes
venues_merged = df_venue.merge(
    df_complexes,
    on="complex_id",
    how="left"
)

# 3. Merge Competitor Rankings with Competitors
rankings_merged = df_competitor_rankings.merge(
    df_competitors,
    on="competitor_id",
    how="left"
)

# View Competitions Dataset
print(f"Number of Rows = {competitions_merged.shape[0]}\nNumber of Columns = {competitions_merged.shape[1]}")
print(f"Null Values = {competitions_merged.isnull().sum().sum()}\nDuplicate Values = {competitions_merged.duplicated().sum()}")
competitions_merged.head()

# View Complexes Dataset
print(f"Number of Rows = {venues_merged.shape[0]}\nNumber of Columns = {venues_merged.shape[1]}")
print(f"Null Values = {venues_merged.isnull().sum().sum()}\nDuplicate Values = {venues_merged.duplicated().sum()}")
venues_merged.head()

# View Double Competitor Rankings Dataset
print(f"Number of Rows = {rankings_merged.shape[0]}\nNumber of Columns = {rankings_merged.shape[1]}")
print(f"Null Values = {rankings_merged.isnull().sum().sum()}\nDuplicate Values = {rankings_merged.duplicated().sum()}")
rankings_merged.head()