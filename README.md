# Trade Assistant System

A functional system for trade duty calculation and procedural guidance.

## Features

- **Duty Calculator:** Calculate import duties and VAT based on HS codes.
- **Trade Assistant Chat:** AI-powered (mocked) assistant for trade queries.
- **Trade Procedures:** Step-by-step guides for import/export.
- **Analytics Dashboard:** Visual representation of trade data.

## Project Structure

- `/public`: Frontend HTML/JS/CSS files.
- `/backend`: Python FastAPI backend.

## Getting Started

### Backend

1. Navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python main.py
   ```

### Frontend

Simply open `public/index.html` in your web browser.

## Backend API Documentation

Once the backend is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
