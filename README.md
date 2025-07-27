# 🎙️ VoicePaper: AI Podcast Generator

[](https://www.python.org/)
[](https://fastapi.tiangolo.com/)
[](https://streamlit.io/)
[](https://www.docker.com/)
[](https://www.postgresql.org/)

VoicePaper is a full-stack, containerized application that transforms online articles and research papers into engaging, on-demand podcasts. It leverages a modern Python-based stack, including a FastAPI backend for processing and a Streamlit frontend for user interaction.

-----

## 🚀 Screenshots
![Podcast app screenshot](https://github.com/RohanThawait/VoicePaper/blob/main/screenshots/Screenshot%202025-07-27%20230815.png)
![Podcast app screenshot](https://github.com/RohanThawait/VoicePaper/blob/main/screenshots/Screenshot%202025-07-27%20230833.png)
![Podcast app screenshot](https://github.com/RohanThawait/VoicePaper/blob/main/screenshots/Screenshot%202025-07-27%20230849.png)

-----

## ✨ Features

  - **URL & PDF Processing:** Generate podcasts from both web articles and uploaded PDF documents.
  - **AI-Powered Summarization:** Uses Google's Gemini API to create concise, podcast-style scripts.
  - **Podcast History:** A full library of previously generated podcasts, stored and retrieved from a PostgreSQL database.
  - **Responsive UI:** An interactive frontend built with Streamlit.

-----

## 🏛️ Architecture

VoicePaper is a multi-service application orchestrated with Docker Compose, featuring a decoupled frontend and backend for scalability and robustness.

```
User (Uploads URL/PDF) --------+
                               |
                               v                   
                +-----------------------------+     +-------------------------------+
                |   Streamlit Frontend        |---->|        FastAPI Backend        |
                | (UI & API Requester)        |     |     (Business Logic)          |
                +-----------------------------+     +-------------------------------+
                                                                |           ^
                                                                |           | (Summary)
                                                                v           |
                +-----------------------------+     +-------------------------------+
                |   PostgreSQL Database       |<----|        AI Pipeline          |
                |  (Stores History & Status)  |     | (Scrape/Extract -> Summarize) |
                +-----------------------------+     +-------------------------------+
                                                                |           ^
                                                                |           | (Text)
                                                                v           |
                                                            +--------------------+
                                                            |   Google Gemini    |
                                                            +--------------------+
```

-----

## 🛠️ Tech Stack

  - **Backend:** FastAPI, PostgreSQL, SQLAlchemy
  - **Frontend:** Streamlit
  - **AI:** Google Gemini API, gTTS
  - **DevOps:** Docker, Docker Compose

-----

## ⚙️ Setup & Installation

To run this project locally, ensure you have Docker and Docker Compose installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/voicepaper.git
    cd voicepaper
    ```

2.  **Create your environment file:**
    In the `/backend` directory, create a `.env` file and add your Gemini API key:

    ```
    GEMINI_API_KEY="your_api_key_here"
    ```

3.  **Run with Docker Compose:**
    From the root directory, run:

    ```bash
    docker-compose up --build
    ```

4.  **Access the application:**

      - **Frontend:** `http://localhost:8501`
      - **Backend API Docs:** `http://localhost:8000/docs`
