import streamlit as st

import newsletter

PDF_PATH = "/Users/JonatanMBA/Documents/code/CityDigest/data"
OPENAI_API_KEY = "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"
COUNTRY = "Switzerland"
CITY = "Zurich"
LEVEL = "don't know much"

st.set_page_config(
    page_title="Echo Echo Zürich",
    page_icon="📣",
    layout="centered"
)

st.title("Echo Echo Zürich")

todaysNews = newsletter.get_newsletter(pdfs_directory=PDF_PATH,
                                       openai_api_key=OPENAI_API_KEY,
                                       country=COUNTRY,
                                       city=CITY,
                                       level=LEVEL)

st.markdown(newsletter.newsletter_mdformat(todaysNews), unsafe_allow_html=True)
newsletter.save_newsletter_mdformat(todaysNews, "newsletter.md")
