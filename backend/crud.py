from sqlalchemy.orm import Session
import models

def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def create_subscription(db: Session, name: str, url: str, user_id: int = 1):
    db_subscription = models.Subscription(subscription_name=name, url=url, user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def create_podcast_record(db: Session, subscription_id: int, title: str):
    db_podcast = models.Podcast(title=title, subscription_id=subscription_id)
    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast

def update_podcast_status(db: Session, podcast_id: int, status: models.PodcastStatus, file_url: str = None):
    db_podcast = db.query(models.Podcast).filter(models.Podcast.id == podcast_id).first()
    if db_podcast:
        db_podcast.status = status
        if file_url:
            db_podcast.audio_file_url = file_url
        db.commit()
    return db_podcast

def get_all_podcasts(db: Session):
    return db.query(models.Podcast).order_by(models.Podcast.created_at.desc()).all()

def get_or_create_pdf_subscription(db: Session, user_id: int = 1):
    pdf_subscription = db.query(models.Subscription).filter_by(
        subscription_name="PDF Uploads", user_id=user_id
    ).first()

    if not pdf_subscription:
        pdf_subscription = create_subscription(
            db, name="PDF Uploads", url="local_pdf", user_id=user_id
        )
    return pdf_subscription