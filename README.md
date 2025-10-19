# AliAI - Halal Banking AI Assistant

## Project Overview

AliAI is an AI-powered financial consultant for Zaman Bank, the first digital Islamic bank in Kazakhstan. The application provides financial advice to users in accordance with Sharia principles. It understands user queries in Russian, Kazakh, and English, and can process both text and voice messages.

## Features

-   **AI Financial Consultant:** Provides financial advice based on Islamic principles.
-   **Multi-language Support:** Understands Russian, Kazakh, and English.
-   **Voice Transcription:** Transcribes user's voice queries into text.
-   **Intent Detection:** Analyzes user's query to understand their intent and redirect them to the appropriate feature.
-   **Static Frontend Pages:** Includes pages for QR code scanning, deposit calculation, personal data management, and user authentication.

## Tech Stack

-   **Backend:** Python with FastAPI
-   **AI:**
    -   OpenAI GPT-4o-mini for natural language understanding and generation.
    -   OpenAI Whisper for voice transcription.
-   **Frontend:** HTML, CSS, JavaScript
-   **Database:** SQLite

## Usage

To run the application, use the following command from the root directory:

```bash
uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Reference

The main API endpoints are defined in `main.py`:

-   `GET /`: Serves the main page of the application.
-   `GET /qr`: Serves the QR code scanner page.
-   `GET /deposit`: Serves the deposit calculator page.
-   `GET /personal-data`: Serves the personal data management page.
-   `GET /auth`: Serves the user authentication page.
-   `POST /transcribe`: Transcribes an audio file to text.
-   `GET /chat`: The main endpoint for the AI assistant. It takes a `message` query parameter with the user's query.
