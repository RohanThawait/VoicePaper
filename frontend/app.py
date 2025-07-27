import streamlit as st
import requests
import os

st.set_page_config(
    page_title="VoicePaper",
    page_icon="🎙️",
    layout="wide"
)

SUBSCRIBE_URL = "http://backend:8000/subscribe"
PDF_URL = "http://backend:8000/generate-from-pdf"
PODCASTS_URL = "http://backend:8000/podcasts"

def get_audio_file_url(path):
    return f"http://localhost:8000/static/{os.path.basename(path)}"

with st.sidebar:
    st.title("About VoicePaper")
    st.info(
        "VoicePaper transforms online articles and research papers "
        "into engaging podcasts."
    )

st.title("🎙️ VoicePaper: Your Personal Podcast Studio")

tab1, tab2 = st.tabs(["New Podcast", "Podcast History"])

with tab1:
    st.header("Create from Article URL")
    with st.form("url_form"):
        url = st.text_input("Article URL")
        name = st.text_input("Subscription Name")
        url_submitted = st.form_submit_button("Generate from URL")

    if url_submitted and url and name:
        with st.spinner("Submitting your request..."):
            try:
                response = requests.post(SUBSCRIBE_URL, json={"url": url, "name": name})
                if response.status_code == 200:
                    st.success(response.json()['message'])
                else:
                    st.error("Failed to submit URL.")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection Error: {e}")

    st.divider()

    st.header("Create from Research Paper")
    uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")

    if uploaded_file:
        if st.button("Generate from PDF"):
            with st.spinner("Uploading and processing your PDF..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(PDF_URL, files=files)
                    if response.status_code == 200:
                        st.success(response.json()['message'])
                    else:
                        st.error("Failed to process PDF.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection Error: {e}")

with tab2:
    st.header("Your Podcast Library")
    st.button("Refresh")

    try:
        response = requests.get(PODCASTS_URL)
        if response.status_code == 200:
            podcasts = response.json()
            if not podcasts:
                st.info("No podcasts found. Generate one from the 'New Podcast' tab!")
            else:
                for podcast in podcasts:
                    if podcast.get('status') == 'COMPLETE':
                        st.subheader(podcast['title'])
                        
                        audio_url = get_audio_file_url(podcast['audio_file_url'])
                        st.audio(audio_url)
                    else:
                        st.subheader(podcast['title'])
                        st.warning(f"Status: {podcast.get('status', 'UNKNOWN')}")
        else:
            st.error("Could not retrieve podcast history.")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the backend: {e}")


