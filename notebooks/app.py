import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

st.set_page_config(page_title="Literary Trends Warehouse", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            font-weight: 600;
        }
        .query-question {
            font-size: 1rem;
            color: #aaaaaa;
            margin-bottom: 1rem;
            font-style: italic;
        }
    </style>
""", unsafe_allow_html=True)

mpl.rcParams['font.family'] = 'DejaVu Sans'

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

st.sidebar.markdown("## Literary Trends")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Choose query to preview", [
    "Home",
    "Top Longest Running Bestsellers",
    "Authors with the Most Bestsellers",
    "Hardcover Fiction Rankings",
    "Most Frequent Authors",
    "Critics vs Bestsellers Overlap",
    "Top Publishers by Shelf Life",
    "Books Over 20 Weeks but Never Top 5",
    "Books That Debuted at Number 1",
    "Authors in Both Critics and Bestsellers"
])

if page == "Home":
    st.title("Literary Trends Warehouse")
    st.write("25+ years of NYT data — explored.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("About This Project")
        st.write("""
            The Literary Trends Warehouse is a Big Data pipeline built for the
            Fundamentals of Data Engineering course. It ingests 25+ years of NYT
            editorial and bestseller data to help readers discover books with lasting
            cultural and critical value.

            Bestseller lists reflect short-term hype — we combine NYT Critics Picks
            with weekly bestseller rankings to surface books that have truly stood
            the test of time.
        """)

    with col2:
        st.subheader("The Data")
        st.write("This project pulls from two NYT APIs:")
        st.markdown("""
        - **NYT Archive API** — Critics Pick reviews from 2000 to 2026
        - **NYT Books API** — Weekly hardcover Fiction and Non-Fiction bestseller rankings from 2008 to 2026
        """)
        st.write("Data is stored in MongoDB, cleaned with Pandas, and loaded into PostgreSQL for analysis.")

    st.divider()
    st.subheader("How to Use This App")
    st.write("""
        Use the dropdown in the left sidebar to explore different views of the data.
        Each view runs a live SQL query against the database and displays the results
        as a table and chart. Some views include interactive sliders so you can filter
        by number of results or other parameters.
    """)
    st.markdown("""
    - Top longest running bestsellers
    - Authors with the most bestsellers
    - Hardcover fiction rankings
    - Most frequent authors
    - Critics vs Bestsellers overlap
    - Top publishers by shelf life
    - Books over 20 weeks but never top 5
    - Books that debuted at number 1
    - Authors in both Critics Picks and Bestsellers
    """)

elif page == "Top Longest Running Bestsellers":
    st.header("Top Longest Running Bestsellers")
    st.markdown('<div class="query-question">Which books stayed on the NYT bestseller list for the most weeks?</div>', unsafe_allow_html=True)
    limit = st.slider("How many books would you like to see?", min_value=5, max_value=25, value=10, step=5)
    df = run_query(f"""
        SELECT title, author, MAX(weeks_on_list) as total_weeks, MIN(rank) as best_rank
        FROM bestsellers
        GROUP BY title, author
        ORDER BY total_weeks DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['title'], df['total_weeks'], color='#2d6a4f')
    ax.set_xlabel("Weeks on List")
    ax.set_title(f"Top {limit} Longest Running Bestsellers")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Authors with the Most Bestsellers":
    st.header("Authors with the Most Unique Bestsellers")
    st.markdown('<div class="query-question">Which authors have had the most unique titles on the bestseller list?</div>', unsafe_allow_html=True)
    limit = st.slider("How many authors would you like to see?", min_value=5, max_value=20, value=10, step=5)
    df = run_query(f"""
        SELECT author, COUNT(DISTINCT title) as unique_bestsellers,
        AVG(weeks_on_list)::NUMERIC(10,2) as avg_weeks_per_book
        FROM bestsellers
        GROUP BY author
        HAVING COUNT(DISTINCT title) > 1
        ORDER BY unique_bestsellers DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df['author'], df['unique_bestsellers'], color='#1d3557')
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Unique Bestsellers")
    ax.set_title(f"Top {limit} Most Prolific Authors")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Hardcover Fiction Rankings":
    st.header("Hardcover Fiction Rankings")
    st.markdown('<div class="query-question">Which hardcover fiction books appeared on the list the most times and how did their ranking change over time?</div>', unsafe_allow_html=True)
    limit = st.slider("How many books would you like to see?", min_value=5, max_value=30, value=20, step=5)
    df = run_query(f"""
        SELECT DISTINCT title, author,
        FIRST_VALUE(rank) OVER (PARTITION BY title ORDER BY list_date ASC) as starting_rank,
        LAST_VALUE(rank) OVER (PARTITION BY title ORDER BY list_date ASC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as current_rank,
        COUNT(*) OVER (PARTITION BY title) as times_on_list
        FROM bestsellers
        WHERE list_name = 'hardcover-fiction'
        ORDER BY times_on_list DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)

elif page == "Most Frequent Authors":
    st.header("Most Frequent Authors on the Bestseller List")
    st.markdown('<div class="query-question">Which authors appear most often across all weekly bestseller lists?</div>', unsafe_allow_html=True)
    limit = st.slider("How many authors would you like to see?", min_value=5, max_value=20, value=10, step=5)
    df = run_query(f"""
        SELECT author, COUNT(*) as appearances
        FROM bestsellers
        GROUP BY author
        ORDER BY appearances DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df['author'], df['appearances'], color='#e63946')
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Appearances")
    ax.set_title(f"Top {limit} Authors by Total Appearances")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Critics vs Bestsellers Overlap":
    st.header("Critics vs Bestsellers Overlap")
    st.markdown('<div class="query-question">Which books were both critically reviewed by the NYT and appeared on the bestseller list?</div>', unsafe_allow_html=True)
    min_reviews = st.slider("Minimum number of critic reviews to filter by", min_value=1, max_value=10, value=1)
    df = run_query(f"""
        SELECT b.title, b.author, MAX(b.weeks_on_list) as max_weeks,
        COUNT(c.headline) as review_count
        FROM bestsellers b
        LEFT JOIN critics c ON LOWER(b.title) = LOWER(c.headline)
        GROUP BY b.title, b.author
        HAVING COUNT(c.headline) >= {min_reviews}
        ORDER BY review_count DESC, max_weeks DESC
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['review_count'], df['max_weeks'], color='#457b9d', alpha=0.6, s=80)
    ax.set_xlabel("Number of Critic Reviews")
    ax.set_ylabel("Max Weeks on List")
    ax.set_title("Do Critic Reviews Lead to More Weeks on List?")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Top Publishers by Shelf Life":
    st.header("Top Publishers by Shelf Life")
    st.markdown('<div class="query-question">Which publishers have produced books that collectively spent the most weeks on the bestseller list?</div>', unsafe_allow_html=True)
    limit = st.slider("How many publishers would you like to see?", min_value=5, max_value=20, value=10, step=5)
    df = run_query(f"""
        SELECT publisher, COUNT(DISTINCT title) as total_unique_books,
        SUM(weeks_on_list) as total_shelf_life
        FROM bestsellers
        GROUP BY publisher
        ORDER BY total_shelf_life DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(df['publisher'], df['total_shelf_life'], color='#6a0572')
    ax.set_xlabel("Total Weeks on List")
    ax.set_title(f"Top {limit} Publishers by Total Shelf Life")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Books Over 20 Weeks but Never Top 5":
    st.header("Books Over 20 Weeks but Never Top 5")
    st.markdown('<div class="query-question">Which books stayed on the list for a long time but never broke into the top 5 rankings?</div>', unsafe_allow_html=True)
    min_weeks = st.slider("Minimum weeks on list to filter by", min_value=20, max_value=60, value=20, step=5)
    df = run_query(f"""
        SELECT title, author, weeks_on_list, rank as final_rank
        FROM bestsellers
        WHERE weeks_on_list > {min_weeks} AND rank > 5
        ORDER BY weeks_on_list DESC
    """)
    st.dataframe(df, use_container_width=True)

elif page == "Books That Debuted at Number 1":
    st.header("Books That Debuted at Number 1")
    st.markdown('<div class="query-question">Which books entered the bestseller list straight at number 1, and how long did they stay?</div>', unsafe_allow_html=True)
    limit = st.slider("How many books would you like to see?", min_value=5, max_value=25, value=10, step=5)
    df = run_query(f"""
        SELECT title, author, list_date, weeks_on_list
        FROM bestsellers
        WHERE rank = 1
        ORDER BY weeks_on_list DESC
        LIMIT {limit}
    """)
    st.dataframe(df, use_container_width=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(df['title'], df['weeks_on_list'], color='#f4a261')
    plt.xticks(rotation=45, ha='right')
    ax.set_ylabel("Weeks on List")
    ax.set_title(f"Top {limit} Number 1 Debuts by Weeks on List")
    plt.tight_layout()
    st.pyplot(fig)

elif page == "Authors in Both Critics and Bestsellers":
    st.header("Authors in Both Critics Picks and Bestsellers")
    st.markdown('<div class="query-question">Which authors have been both critically recognized by NYT reviewers and appeared on the weekly bestseller list?</div>', unsafe_allow_html=True)
    df = run_query("""
        SELECT DISTINCT b.author
        FROM bestsellers b
        INNER JOIN critics c ON LOWER(b.author) LIKE LOWER('%' || c.byline || '%')
        ORDER BY b.author
        LIMIT 10
    """)
    st.dataframe(df, use_container_width=True)