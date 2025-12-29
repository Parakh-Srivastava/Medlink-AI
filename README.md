# 🏥 AI First Aid Assistant

A smart web application that provides immediate first-aid instructions using a **Cache-Aside** logic: checking a local SQL database first, then a hardcoded map, and finally falling back to the **Gemini 2.0 AI** for new emergencies.

## 🚀 Features
- **Smart Search:** Detects keywords (like "burn", "cut", "sting") within natural language user queries.
- **AI Integration:** Uses Google Gemini 2.0 Flash to generate structured medical JSON responses for unknown emergencies.
- **SQL Caching:** Automatically saves new AI responses to a SQLite database to save API costs and improve speed.
- **Responsive UI:** Built with HTML5, CSS3, and Bootstrap for mobile-friendly emergency access.

## 🛠️ Tech Stack
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Backend:** Python (Flask)
- **Database:** SQL (SQLite + SQLAlchemy ORM)
- **AI Model:** Google Gemini 2.0 Flash SDK (`google-genai`)

## 📂 Project Structure
```text
├── app.py              # Main Flask application logic
├── promt.py            # AI class & Gemini API integration
├── emergencyData.py    # Pre-defined emergency map (FastKey)
├── database.db         # SQLite database file (auto-generated)
├── templates/
│   └── index.html      # Main frontend interface
├── static/
│   └── styles.css      # Custom styling
└── .env                # API Key storage (ignored by git)
