import streamlit as st
import requests
from config import ACCESS_KEY, REGIONS  # Import ACCESS_KEY and REGIONS from the config file

# Set the API endpoints
LIVE_NEWS_API = "https://api.mediastack.com/v1/news"
HISTORICAL_NEWS_API = "https://api.mediastack.com/v1/news"
NEWS_SOURCES_API = "https://api.mediastack.com/v1/sources"

# Create a Streamlit sidebar for user input
st.sidebar.title("Agriculture News in India")
selected_tab = st.sidebar.radio("Select Section", ["Live News", "Historical News", "News Sources"])

if selected_tab == "Live News":
    # Display live news options
    sources = st.sidebar.text_input("Specify News Sources (comma-separated)")
    categories = st.sidebar.multiselect("Select Categories", ["general", "business", "entertainment", "health", "science", "sports", "technology"])
    countries = st.sidebar.text_input("Specify Countries (comma-separated 2-letter codes)")
    languages = st.sidebar.text_input("Specify Languages (comma-separated 2-letter codes)")
    keywords = st.sidebar.text_input("Search Keywords (comma-separated)")

elif selected_tab == "Historical News":
    historical_date = st.sidebar.date_input("Select Historical Date")
    if historical_date:
        historical_date_str = historical_date.strftime("%Y-%m-%d")
        sources = st.sidebar.text_input("Specify News Sources (comma-separated)")
        categories = st.sidebar.multiselect("Select Categories", ["general", "business", "entertainment", "health", "science", "sports", "technology"])
        countries = st.sidebar.text_input("Specify Countries (comma-separated 2-letter codes)")
        languages = st.sidebar.text_input("Specify Languages (comma-separated 2-letter codes)")
        keywords = st.sidebar.text_input("Search Keywords (comma-separated)")

# Fetch and display news based on user preferences
if selected_tab == "Live News" or selected_tab == "Historical News":
    if selected_tab == "Live News":
        API_ENDPOINT = LIVE_NEWS_API
    else:
        API_ENDPOINT = HISTORICAL_NEWS_API

    params = {
        "access_key": ACCESS_KEY,
        "countries": "in",  # Limit to India
        "languages": "en",  # English language news
        "limit": 10,
        "sort": "published_desc"
    }

    # Add user-specified filters
    if sources:
        params["sources"] = sources
    if categories:
        params["categories"] = ",".join(categories)
    if countries:
        params["countries"] = countries
    if languages:
        params["languages"] = languages
    if keywords:
        params["keywords"] = keywords

    if selected_tab == "Historical News" and historical_date:
        params["date"] = historical_date_str

    response = requests.get(API_ENDPOINT, params=params)

    if response.status_code == 200:
        data = response.json()["data"]

        st.title("Agriculture News")
        if data:
            for article in data:
                st.write("## " + article["title"])
                st.write("Published by:", article["source"])
                st.write("Description:", article["description"])
                st.write("Published Date:", article["published_at"])
                st.image(article["image"])
        else:
            st.write("No news data available. Please check your filters.")
    else:
        st.error("Error fetching news data.")

elif selected_tab == "News Sources":
    search_query = st.sidebar.text_input("Search News Sources")
    if search_query:
        params = {
            "access_key": ACCESS_KEY,
            "search": search_query,
            "limit": 10,
            "offset": 0
        }
        response = requests.get(NEWS_SOURCES_API, params=params)

        if response.status_code == 200:
            data = response.json()["data"]

            st.title("News Sources")
            if data:
                for source in data:
                    st.write("## " + source["name"])
                    st.write("Category:", source["category"])
                    st.write("Country:", source["country"])
                    st.write("Language:", source["language"])
                    st.write("URL:", source["url"])
            else:
                st.write("No news sources found for your search query.")
        else:
            st.error("Error fetching news sources data.")
