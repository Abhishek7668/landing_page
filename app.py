import streamlit as st
import requests
import google.generativeai as genai

# 🔐 Gemini API Key
genai.configure(api_key="AIzaSyAYAKCyreKVe36vS2BKfRcMk_1jbg29NHA")

model = genai.GenerativeModel("gemini-2.5-flash")

st.title("AI Landing Page Personalizer")

# 🔹 Inputs
ad = st.text_area("Paste Ad Creative")
url = st.text_input("Landing Page URL")


# 🔹 Simple scraper (same as before)
def scrape_page(url):
    return {
        "title": "Demo Page",
        "headline": "Welcome to Our Product",
        "text": "This is a high-quality solution designed for modern users."
    }


# 🔹 Gemini AI function
def personalize(ad, page):
    prompt = f"""
You are a CRO expert.

Ad:
{ad}

Landing Page:
Headline: {page['headline']}
Text: {page['text']}

Task:
Rewrite the headline and create a better CTA based on the ad.
Keep meaning similar.
Do not invent features.

Output format:
Headline:
CTA:
"""

    response = model.generate_content(prompt)
    return response.text


# 🔹 Main button
if st.button("Generate", key="generate_btn"):

    if not ad or not url:
        st.warning("Please enter both Ad and URL")
    else:
        page = scrape_page(url)
        result = personalize(ad, page)

        # 🔹 Original
        st.subheader("Original Page")
        st.markdown(f"### {page['headline']}")
        st.write(page['text'])

        # 🔹 Safe parsing
        lines = result.split("\n")

        new_headline = ""
        cta = "Click Here"

        for line in lines:
            if "Headline:" in line:
                new_headline = line.replace("Headline:", "").strip()
            if "CTA:" in line:
                cta = line.replace("CTA:", "").strip()

        # 🔹 Personalized Output
        st.subheader("✨ Personalized Page")

        st.markdown(f"# {new_headline}")
        st.write(page['text'])

        st.button(cta, key="cta_button")