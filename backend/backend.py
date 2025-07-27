import os
import shutil
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import crud, models
from database import get_db
from pipeline import run_url_pipeline, run_pdf_pipeline
from database import engine, SessionLocal

# Creates all tables from your models
models.Base.metadata.create_all(bind=engine)


def create_initial_user():
    db = SessionLocal()
    user = db.query(models.User).filter(models.User.id == 1).first()
    if not user:
        new_user = models.User(id=1, email="test@example.com")
        db.add(new_user)
        db.commit()
        print("INFO:     Dummy user with id=1 created.")
    db.close()

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_initial_user()
    
class SubscriptionRequest(BaseModel):
    url: str
    name: str

@app.post("/subscribe")
async def subscribe_from_url(
    request: SubscriptionRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    subscription = crud.create_subscription(db, name=request.name, url=request.url)
    background_tasks.add_task(run_url_pipeline, subscription_id=subscription.id)
    return {"message": "Subscription received! Your podcast is being generated."}

@app.post("/generate-from-pdf")
async def generate_from_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pdf_subscription = crud.get_or_create_pdf_subscription(db)
    
    podcast_record = crud.create_podcast_record(
        db,
        title=file.filename,
        subscription_id=pdf_subscription.id
    )

    background_tasks.add_task(run_pdf_pipeline, podcast_id=podcast_record.id, pdf_path=file_path)
    return {"message": "PDF received! Your podcast is being generated."}

@app.get("/podcasts")
async def get_podcast_history(db: Session = Depends(get_db)):
    return crud.get_all_podcasts(db)
