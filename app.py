import streamlit as st
import os
from ai_core import (
    extract_text_from_pdfs,
    summarize_text_with_gemini,
    generate_audio_with_gtts,
)
 
PODCAST_PROMPT_TEMPLATE = """
You are an expert science communicator and podcast host. Your task is to transform the following complex research paper text into a clear, engaging, and concise 5-minute podcast script.

Focus on the key findings, the "so what" factor, and the main takeaways. Avoid jargon. Explain complex ideas in simple terms. Structure the output as a script, with a brief intro, a main body explaining the research, and a short, impactful conclusion.

Here is the research paper text:
---
{text}
---
"""
# Define a directory to save temporary files
TEMP_DIR = "temp"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# --- Streamlit App Interface ---

st.set_page_config(page_title="VoicePaper", page_icon="🎙️")
st.title("🎙️ VoicePaper: Research to Podcast")
st.write(
    "Welcome! Upload a research paper (PDF) and get a podcast-style audio summary."
)

# 1. File Uploader
uploaded_file = st.file_uploader(
    "Upload your research paper (PDF)", 
    type="pdf"
)

# Place your background music in the project folder
background_music_file = "C:/Users/Rohan/Projects/Project_6/VoicePaper/short-10-228139.mp3" # Change this if your file has a different name

if uploaded_file is not None:
    # 2. Generate Button
    if st.button("Generate Podcast"):
        with st.spinner("Generating your podcast... This may take a few moments."):
            try:
                # Save the uploaded file to a temporary path
                temp_pdf_path = os.path.join(TEMP_DIR, uploaded_file.name)
                with open(temp_pdf_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # --- Run the AI Pipeline ---
                st.info("Step 1: Extracting text from PDF...")
                extracted_text = extract_text_from_pdfs([temp_pdf_path])

                st.info("Step 2: Summarizing text with AI...")
                summary_text = summarize_text_with_gemini(extracted_text, PODCAST_PROMPT_TEMPLATE)

                st.info("Step 3: Generating speech...")
                speech_audio_path = os.path.join(TEMP_DIR, "speech.mp3")
                generate_audio_with_gtts(summary_text, speech_audio_path)

                #st.info("Step 4: Adding background music...")
                #final_audio_path = os.path.join(TEMP_DIR, "final_podcast.mp3")
                #add_background_music(speech_audio_path, background_music_file, final_audio_path)
                
                # --- Display the Final Output ---
                st.success("Podcast generated successfully!")
                st.audio(speech_audio_path, format='audio/mp3')

                # Provide a download button
                with open(speech_audio_path, "rb") as file:
                    st.download_button(
                        label="Download Podcast",
                        data=file,
                        file_name="podcast_summary.mp3",
                        mime="audio/mp3"
                    )

            except Exception as e:
                st.error(f"An error occurred: {e}")

            # Clean up temporary files
            finally:
                for file_in_dir in os.listdir(TEMP_DIR):
                    os.remove(os.path.join(TEMP_DIR, file_in_dir))