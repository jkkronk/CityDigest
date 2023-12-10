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

newsletter_md = newsletter.newsletter_mdformat(todaysNews, OPENAI_API_KEY)

# Show and save
st.markdown(newsletter_md, unsafe_allow_html=True)
with open("generated/newsletter.md", "w") as f:
    f.write(newsletter_md)
