# **Fundamentals of Data Engineering — Literary Warehouse Project**
*Hritika Singh & Hanah Shih*

## Overview
A Big Data pipeline that ingests 25+ years of NYT editorial and bestseller data to help readers discover books with lasting cultural and critical value. The system combines NYT Critics' Picks (editorial signal) with Bestseller Rankings (market signal) to surface books that have truly stood the test of time.

## Repository Structure
'''
literary/
├── notebooks/
│   ├── 01_ingestion.ipynb       # Pulls data from NYT APIs into MongoDB
│   ├── 02_cleaning.ipynb        # Cleans data with Pandas, exports CSVs
│   ├── critics_clean.csv        # Cleaned Critics' Picks data
│   └── bestsellers_clean.csv    # Cleaned Bestsellers data
├── db/
│   └── placeholder.txt          # Placeholder file for now, will be replaced with schema.sql for PostgreSQL table definitions
├── .gitignore
├── requirements.txt
└── README.md
'''

## Tech Stack
- **Python** — Primary ETL engine
- **MongoDB** — NoSQL staging layer for raw API data
- **PostgreSQL** — Relational store for cleaned data and SQL analysis
- **Neo4j** — Graph database for author/genre/critic relationships
- **Pandas** — Data cleaning and transformation
- **Streamlit + FastAPI** — Frontend and API interface


## Data Sources
- **NYT Archive API** — Critics' Pick reviews (2000–2026)
- **NYT Books API** — Weekly hardcover Fiction & Non-Fiction bestseller rankings (2008–2026)

## Getting Started
### Step 1: Setting Up Environment & Installing All Dependencies
  1. In terminal, navigate to the GitHub repo folder and install requirements.txt to ensure all libraries are installed before starting development.
  2. eg: cd Documents/GitHub/literary pip install -r requirements.txt

### Step 2: Data Ingestion & Setting Up MongoDB
  1. Start both Docker & MongoDB Compass. Connect to local host in MongoDB
  2. If you haven't already, create an account on NYT Developers API to be able to access the Archive and Books APIs. https://developer.nytimes.com/apis
  3. Create a new app called "Literary Trends Project" in your account and enable both Archive and Books APIs and create the API key.
  4. Once the key is created, open Jupyter notebooks through Anaconda and route to the GitHub repository and begin code for data ingestion, under the name '01_ingestion.ipynb'

### Step 3: 01_ingestion.ipynb – Ingesting Archive & Books API data and loading into MongoDB
  1. Download all packages
  2. Connect to MongoDB
  3. Connect to API Key & define fetching function
  4. Insert data into MongoDB

### Step 4: 02_cleaning.ipynb – Cleaning & Transformation
  1. Download all packages
  2. Connect to MongoDB
  3. Convert db to dataframe for both datasets
  4. Proceed with cleaning – Keeping only relevant columns, removing null values, removing unnecessary text, etc.
  5. Export both as .csv files for SQL querying
