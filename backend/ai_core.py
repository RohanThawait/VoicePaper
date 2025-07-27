import os
from typing import List

import google.generativeai as genai
import pymupdf
from dotenv import load_dotenv
from gtts import gTTS

load_dotenv()

PODCAST_PROMPT_TEMPLATE = """
You are an expert science communicator and podcast host. Your task is to transform the following complex research paper text into a clear, engaging, and concise 5-minute podcast script.

Focus on the key findings, the "so what" factor, and the main takeaways. Avoid jargon. Explain complex ideas in simple terms. Structure the output as a script, with a brief intro, a main body explaining the research, and a short, impactful conclusion.

Here is the research paper text:
---
{text}
---
"""

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        with pymupdf.open(pdf_path) as doc:
            return "".join(page.get_text() for page in doc)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def summarize_text_with_gemini(text_to_summarize: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        full_prompt = PODCAST_PROMPT_TEMPLATE.format(text=text_to_summarize)
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return ""

def generate_audio_with_gtts(text_to_speak: str, output_path: str):
    try:
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        tts.save(output_path)
        print(f" Audio successfully saved to {output_path}")
    except Exception as e:
        print(f" An error occurred during audio generation: {e}")
