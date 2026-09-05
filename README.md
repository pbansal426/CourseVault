# CourseVault

**Status: in development.**

An online course platform (Flask + SQLAlchemy) where schools can register, students get free
access through their school, and course creators can upload content — chapters, videos, a
discussion forum. Planned: an AI assistant trained per-course to help students with the material.

## Stack

Python, Flask, Flask-Login, Flask-SQLAlchemy, SQLite/SQL for user data, HTML/CSS/JS frontend.

## Running

```bash
cd code
pipx install poetry   # if not already installed
poetry install
python3 main.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Roadmap

1. Finish SQL models
2. Completion tracking for users
3. AI chatbot for course content (Ollama or an OpenAI-compatible API)
