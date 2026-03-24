# SkillSnacks Engineering Specification
Codex Implementation Guide

---

## 1. Project Overview

SkillSnacks is a micro-learning web application designed to help users explore interesting ideas through short lessons that can be completed in 5–10 minutes.

The application encourages a daily curiosity habit by allowing users to discover lessons through:

- topics
- categories
- daily lessons
- random discovery
- search

Each lesson focuses on a single idea and explains:

- why it matters
- the key concepts
- a curiosity hook

The platform should remain simple, lightweight, and content-focused.

---

## 2. Learning Model

SkillSnacks follows a structured curiosity model:

Topic  
→ Lessons  
→ Ideas  
→ Curiosity Hook

Lessons are intentionally short so they can be consumed quickly and frequently.

---

## 3. Technology Stack

Backend:
- Python
- Flask

Frontend:
- HTML
- CSS
- Minimal JavaScript

Storage:
- File-based JSON content
- No database required

---

## 4. System Architecture

Browser  
↓  
Flask Application  
↓  
Lesson Engine / Topic Engine / Search Engine  
↓  
JSON Lesson Files

This architecture supports many lessons without complex infrastructure.

---

## 5. Project Directory Structure

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

## 6. Lesson Data Format

Lessons are stored as JSON files.

Example:

{
  "slug": "big-bang",
  "title": "The Big Bang",
  "category": "science",
  "time": "5 minutes",
  "why": "Explains the origin of the universe.",
  "ideas": [
    "The universe began 13.8 billion years ago",
    "Space expanded rapidly",
    "Galaxies formed as matter cooled"
  ],
  "hook": "The atoms in your body were forged in exploding stars.",
  "topics": ["cosmic_origins"]
}

Required fields:
- slug
- title
- category
- time
- why
- ideas
- hook

Optional fields:
- topics

---

## 7. Topic Data Format

Topics represent curated learning tracks.

Example:

{
  "topic_id": "abby_medical_terminology",
  "title": "Abby's Medical Terminology",
  "description": "Beginner introduction to medical terminology.",
  "lessons": [
    "medical_intro",
    "medical_root_words",
    "medical_prefixes",
    "medical_suffixes"
  ]
}

Required fields:
- topic_id
- title
- description
- lessons

---

## 8. Lesson Engine

The lesson engine is responsible for:

- loading JSON lesson files
- indexing lessons by slug
- grouping lessons by category
- returning lessons for routes
- providing ordered lesson lookup
- supporting navigation logic

The lesson loader should run when the app starts.

---

## 9. Topics Engine

The topics loader is responsible for:

- loading topic JSON files
- validating lesson references
- resolving ordered lessons
- returning topics for topic routes
- exposing a list of all topics

Topics must not reference non-existent lessons.

---

## 10. Search Engine

The search engine is responsible for searching across lesson files.

Search fields:
- title
- ideas
- hook

Search should remain simple and file-based.

No external search service should be introduced.

---

## 11. Core Routes

### Home
/
Displays:
- site title
- featured lesson
- daily curiosity lesson
- categories
- topics
- continue learning section if available
- recent or featured lesson cards

### Category
/category/<category_name>
Displays all lessons in the category.

### Lesson
/lesson/<slug>
Displays:
- title
- category
- time
- why
- ideas
- hook
- previous / next navigation
- read-aloud controls

### Topics Index
/topics
Displays all available topics.

### Topic Page
/topic/<topic_id>
Displays:
- topic title
- topic description
- ordered lesson list

### Daily Curiosity
/daily
Displays the lesson selected for the current day.

Daily selection logic must be deterministic.

Preferred implementation:
hash(current_date_string) % total_lessons

### Random Discovery
/random
Redirects to a randomly selected lesson.

### Search
/search?q=<keyword>
Displays matching lessons.

---

## 12. Lesson Page Layout

Each lesson page should contain:

- Title
- Category
- Reading Time
- Why This Matters
- Key Ideas
- Curiosity Hook
- Read Aloud controls
- Previous / Next navigation

The lesson content should be wrapped in a container that supports read-aloud extraction.

---

## 13. Read Aloud Mode

The lesson page must support read-aloud mode using the browser Web Speech API.

Controls:
- Read
- Pause
- Stop

The implementation must be client-side only.

No server-side text-to-speech service should be used.

---

## 14. Continue Learning

The application should remember the last lesson viewed using browser localStorage.

Expected behavior:
- save lesson slug on lesson page load
- home page displays a Continue Learning card if a last lesson exists

---

## 15. UI Principles

The interface should prioritize readability and simplicity.

Design goals:
- large readable text
- centered content column
- mobile-friendly layout
- minimal distractions
- clear lesson cards
- visible navigation

---

## 16. Lesson Cards

Lesson cards should appear on:
- home page
- category pages
- topic pages
- search results

A card should show:
- title
- category
- reading time
- short why summary or preview
- link to read the lesson

---

## 17. Implementation Order

Codex should implement the application in this order:

1. Project structure
2. Lesson loader
3. Topic loader
4. Search engine
5. Flask routes
6. Templates
7. Lesson navigation
8. Continue learning
9. Read-aloud feature
10. Styling
11. Seed content
12. Final QA

---

## 18. Success Criteria

The implementation is successful when:

- the homepage loads
- categories render correctly
- topics render correctly
- lessons render correctly
- daily lesson works
- random discovery works
- search works
- previous / next navigation works
- continue learning works
- read-aloud mode works
- sample content is included

---

## 19. Non-Goals

Codex must not introduce:
- databases
- authentication
- admin panels
- APIs beyond Flask routes
- heavy front-end frameworks
- server-side speech services

This is a lightweight MVP.