# SkillSnacks

SkillSnacks is a micro-learning web application designed to help users explore interesting ideas through short lessons that can be completed in 5–10 minutes.

The platform encourages a daily curiosity habit by allowing users to discover lessons through:

- topics
- categories
- daily lessons
- random discovery
- search
- read-aloud mode

Each lesson focuses on a single idea and explains:

- why it matters
- the key concepts
- a curiosity hook

The application is intentionally lightweight and content-focused.

---

## Core Features

- Daily curiosity lesson
- Random lesson discovery
- Topic-based browsing
- Category navigation
- Lesson search
- Next / previous lesson navigation
- Read-aloud mode
- Mobile-friendly UI
- Lesson cards for readability
- Continue learning (local browser storage)

---

## Technology Stack

Backend:
- Python
- Flask

Frontend:
- HTML
- CSS
- Minimal JavaScript

Storage:
- File-based JSON lesson system
- No database required

---

## Project Structure

skillsnacks
│
├── app
│   ├── app.py
│   ├── lesson_loader.py
│   ├── topics_loader.py
│   ├── search_engine.py
│
├── templates
│   ├── home.html
│   ├── lesson.html
│   ├── category.html
│   ├── topics.html
│   ├── topic.html
│   └── search.html
│
├── static
│   ├── css
│   │   └── style.css
│   └── js
│       └── speech.js
│
├── lessons
├── topics
├── docs
├── requirements.txt
└── README.md

---

## Local Development Setup

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python app\app.py

Open in browser:

http://127.0.0.1:5000

---

## Product Philosophy

SkillSnacks should feel like snacking on ideas.

Learning should be:

- quick
- interesting
- accessible
- habit-forming

---

## Author

Ray Austria