import os
from database import SessionLocal
import crud, models
from newspaper import Article
from ai_core import (
    extract_text_from_pdf,
    summarize_text_with_gemini,
    generate_audio_with_gtts
)

def scrape_article_text(url: str) -> str:
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return article.text
        
    except Exception as e:
        print(f" Failed to scrape {url}. Error: {e}")
        return ""

def run_url_pipeline(subscription_id: int):
    db = SessionLocal()
    podcast_record = None
    try:
        subscription = crud.get_subscription(db, subscription_id)
        if not subscription:
            raise Exception("Subscription not found")

        article_text = scrape_article_text(subscription.url)
        if not article_text:
            raise Exception("Failed to scrape article")

        podcast_record = crud.create_podcast_record(
            db,
            title=subscription.subscription_name
        )
        
        summary_text = summarize_text_with_gemini(article_text)
        
        audio_path = f"audio_files/podcast_{podcast_record.id}.mp3"
        os.makedirs("audio_files", exist_ok=True)
        generate_audio_with_gtts(summary_text, audio_path)
        
        crud.update_podcast_status(
            db,
            podcast_id=podcast_record.id,
            status=models.PodcastStatus.COMPLETE,
            file_url=audio_path
        )
    except Exception as e:
        if podcast_record:
            crud.update_podcast_status(
                db,
                podcast_id=podcast_record.id,
                status=models.PodcastStatus.FAILED
            )
    finally:
        db.close()

def run_pdf_pipeline(podcast_id: int, pdf_path: str):
    db = SessionLocal()
    try:
        # Update the status to 'PROCESSING'
        crud.update_podcast_status(db, podcast_id, models.PodcastStatus.PROCESSING)
        
        # 1. Extract text from the PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        if not extracted_text:
            raise Exception("Failed to extract text from PDF")

        # 2. Summarize the text
        summary_text = summarize_text_with_gemini(extracted_text)
        
        # 3. Generate the audio file
        audio_path = f"audio_files/podcast_{podcast_id}.mp3"
        os.makedirs("audio_files", exist_ok=True)
        generate_audio_with_gtts(summary_text, audio_path)
        
        # 4. Update the database record to 'COMPLETE'
        crud.update_podcast_status(
            db,
            podcast_id=podcast_id,
            status=models.PodcastStatus.COMPLETE,
            file_url=audio_path
        )
        print(f" Successfully generated podcast for PDF {pdf_path}")

    except Exception as e:
        print(f" Pipeline failed for PDF {pdf_path}: {e}")
        # Mark the podcast as 'FAILED' in the database
        crud.update_podcast_status(db, podcast_id, models.PodcastStatus.FAILED)
    finally:
        # Clean up the temporary PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        db.close()