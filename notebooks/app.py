import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Literary Trends Warehouse", layout="wide")

def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='bestsellers',
        user='postgres',
        password='123456'
    )

conn = get_connection()

def run_query(query):
    return pd.read_sql_query(query, conn)

st.title("Literary Trends Warehouse")
st.write("Explore 25+ years of NYT Critics Picks and Bestseller data.")

page = st.sidebar.selectbox("Choose a View", [
    "Top 10 Longest Running Bestsellers",
    "Authors with the Most Bestsellers",
    "Hardcover Fiction Rankings",
    "Most Frequent Authors",
    "Critics vs Bestsellers Overlap",
    "Top Publishers by Shelf Life",
    "Books Over 20 Weeks but Never Top 5",
    "Books That Debuted at Number 1",
    "Publishers: Fiction vs Nonfiction",
    "Authors in Both Critics and Bestsellers"
])

if page == "Top 10 Longest Running Bestsellers":
    st.header("Top 10 Longest Running Bestsellers")
    df = run_query("""
        SELECT title, author, MAX(weeks_on_list) as total_weeks, MIN(rank) as best_rank
        FROM bestsellers
        GROUP BY title, author
        ORDER BY total_weeks DESC
        LIMIT 10
    """)
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.barh(df['title'], df['total_weeks'], color='teal')
    ax.set_xlabel("Weeks on List")
    ax.set_title("Top 10 Longest Running Bestsellers")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Authors with the Most Bestsellers":
    st.header("Authors with the Most Unique Bestsellers")
    df = run_query("""
        SELECT author, COUNT(DISTINCT title) as unique_bestsellers,
        AVG(weeks_on_list)::NUMERIC(10,2) as avg_weeks_per_book
        FROM bestsellers
        GROUP BY author
        HAVING COUNT(DISTINCT title) > 1
        ORDER BY unique_bestsellers DESC
        LIMIT 10
    """)
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.bar(df['author'], df['unique_bestsellers'], color='steelblue')
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Unique Bestsellers")
    ax.set_title("Authors with the Most Unique Bestsellers")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Hardcover Fiction Rankings":
    st.header("Hardcover Fiction - Most Weeks on List")
    df = run_query("""
        SELECT DISTINCT title, author,
        FIRST_VALUE(rank) OVER (PARTITION BY title ORDER BY list_date ASC) as starting_rank,
        LAST_VALUE(rank) OVER (PARTITION BY title ORDER BY list_date ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as current_rank,
        COUNT(*) OVER (PARTITION BY title) as times_on_list
        FROM bestsellers
        WHERE list_name = 'hardcover-fiction'
        ORDER BY times_on_list DESC
        LIMIT 20
    """)
    st.dataframe(df)

elif page == "Most Frequent Authors":
    st.header("Most Frequent Authors on the Bestseller List")
    df = run_query("""
        SELECT author, COUNT(*) as appearances
        FROM bestsellers
        GROUP BY author
        ORDER BY appearances DESC
        LIMIT 10
    """)
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.bar(df['author'], df['appearances'], color='coral')
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Appearances")
    ax.set_title("Most Frequent Authors on the Bestseller List")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Critics vs Bestsellers Overlap":
    st.header("Books That Were Both Critically Reviewed and Bestsellers")
    df = run_query("""
        SELECT b.title, b.author, MAX(b.weeks_on_list) as max_weeks,
        COUNT(c.headline) as review_count
        FROM bestsellers b
        LEFT JOIN critics c ON LOWER(b.title) = LOWER(c.headline)
        GROUP BY b.title, b.author
        HAVING COUNT(c.headline) > 0
        ORDER BY review_count DESC, max_weeks DESC
    """)
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.scatter(df['review_count'], df['max_weeks'], color='teal', alpha=0.5)
    ax.set_xlabel("Number of Critic Reviews")
    ax.set_ylabel("Max Weeks on List")
    ax.set_title("Do Critic Reviews Lead to More Weeks on List?")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Top Publishers by Shelf Life":
    st.header("Top 10 Publishers by Total Shelf Life")
    df = run_query("""
        SELECT publisher, COUNT(DISTINCT title) as total_unique_books,
        SUM(weeks_on_list) as total_shelf_life
        FROM bestsellers
        GROUP BY publisher
        ORDER BY total_shelf_life DESC
        LIMIT 10
    """)
    st.dataframe(df)
    fig, ax = plt.subplots()
    ax.barh(df['publisher'], df['total_shelf_life'], color='purple')
    ax.set_xlabel("Total Weeks on List")
    ax.set_title("Top Publishers by Total Shelf Life")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Books Over 20 Weeks but Never Top 5":
    st.header("Books on List Over 20 Weeks but Never Ranked in Top 5")
    df = run_query("""
        SELECT title, author, weeks_on_list, rank as final_rank
        FROM bestsellers
        WHERE weeks_on_list > 20 AND rank > 5
        ORDER BY weeks_on_list DESC
    """)
    st.dataframe(df)

elif page == "Books That Debuted at Number 1":
    st.header("Books That Debuted at Number 1")
    df = run_query("""
        SELECT title, author, list_date, weeks_on_list
        FROM bestsellers
        WHERE rank = 1
        ORDER BY weeks_on_list DESC
        LIMIT 10
    """)
    st.dataframe(df)

elif page == "Publishers: Fiction vs Nonfiction":
    st.header("Most Prolific Publishers: Fiction vs Nonfiction")
    df = run_query("""
        SELECT publisher, list_name, COUNT(DISTINCT title) as total_titles
        FROM bestsellers
        GROUP BY publisher, list_name
        ORDER BY total_titles DESC
        LIMIT 10
    """)
    st.dataframe(df)
    fiction = df[df['list_name'] == 'hardcover-fiction']
    nonfiction = df[df['list_name'] == 'hardcover-nonfiction']
    fig, ax = plt.subplots()
    x = range(len(fiction))
    ax.bar(x, fiction['total_titles'].values, width=0.4, label='Fiction', color='steelblue', alpha=0.7)
    ax.bar([i + 0.4 for i in x], nonfiction['total_titles'].values[:len(fiction)], width=0.4, label='Nonfiction', color='coral', alpha=0.7)
    ax.set_xticks([i + 0.2 for i in x])
    ax.set_xticklabels(fiction['publisher'].values, rotation=45, ha='right')
    ax.set_ylabel("Total Titles")
    ax.set_title("Publishers: Fiction vs Nonfiction")
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Authors in Both Critics and Bestsellers":
    st.header("Authors Who Appear in Both Critics Picks and Bestsellers")
    df = run_query("""
        SELECT DISTINCT b.author
        FROM bestsellers b
        INNER JOIN critics c ON LOWER(b.author) LIKE LOWER('%' || c.byline || '%')
        ORDER BY b.author
        LIMIT 10
    """)
    st.dataframe(df)