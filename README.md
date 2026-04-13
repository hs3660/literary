# Literary Warehouse
Fundamentals of Data Engineering

## Step 1: Setting Up Environment & Installing All Dependencies
  1. In terminal, navigate to the GitHub repo folder and install requirements.txt to ensure all libraries are installed before starting development.
  2. eg: cd Documents/GitHub/literary pip install -r requirements.txt

## Step 2: Data Ingestion & Setting Up MongoDB
  1. Start both Docker & MongoDB Compass. Connect to local host in MongoDB
  2. If you haven't already, create an account on NYT Developers API to be able to access the Archive and Books APIs. https://developer.nytimes.com/apis
  3. Create a new app called "Literary Trends Project" in your account and enable both Archive and Books APIs and create the API key.
  4. Once the key is created, open Jupyter notebooks through Anaconda and route to the GitHub repository and begin code for data ingestion, under the name '01_ingestion.ipynb'

## Step 3: 01_ingestion.ipynb
  1. Download all packages
  2. Connect to MongoDB
  3. Connect to API Key & define fetching function
  4. Insert data into MongoDB
