# AGENTS.md

## Purpose

This file provides implementation guidance for AI coding agents working on the SkillSnacks project.

Agents must follow the architectural principles and implementation rules defined here when generating or modifying code.

Agents should prioritize maintaining project structure, readability, and deterministic behavior over introducing unnecessary complexity.

---

## Project Summary

SkillSnacks is a micro-learning platform that delivers short lessons designed to build a daily curiosity habit.

The platform supports:

- lesson browsing
- category navigation
- curated learning tracks (topics)
- daily curiosity lessons
- random discovery
- lesson search
- read-aloud functionality
- continue learning

---

## Core Learning Model

SkillSnacks follows this model:

Topic  
→ Lessons  
→ Ideas  
→ Curiosity Hook

Lessons are intentionally designed to be completed in 5–10 minutes.

Agents must preserve this structure when generating lesson-related features.

---

## Architectural Principles

### 1. Keep the architecture simple
Do not introduce:
- databases
- ORMs
- React, Vue, Angular, or other front-end frameworks
- background workers
- complex caching systems

### 2. Preserve the file-based content system
Lessons must always be loaded from the lessons directory.

### 3. Maintain modular loaders
Keep these modules separate:
- lesson_loader.py
- topics_loader.py
- search_engine.py

### 4. Favor deterministic behavior
Daily lesson selection must be deterministic.

### 5. Preserve lesson schema
Required lesson fields:
- slug
- title
- category
- time
- why
- ideas
- hook

Optional:
- topics

### 6. Preserve topic schema
Required topic fields:
- topic_id
- title
- description
- lessons

---

## Implementation Guidelines

Agents should implement features in this order:
1. Loaders
2. Routes
3. Templates
4. JavaScript
5. Styling

Do not build UI-first without backend support.

---

## Code Style Guidelines

### Python
- Prefer simple functions over unnecessary classes
- Keep files small and readable
- Use clear function names
- Add lightweight comments where useful
- Avoid overengineering

### HTML
- Use semantic structure
- Keep templates readable
- Do not bury content in overly nested markup

### JavaScript
- Keep JavaScript minimal
- Use it only where needed, especially for read-aloud and localStorage features

### CSS
- Keep styling simple and readable
- Mobile-first if practical
- Focus on content layout, spacing, and legibility

---

## Read Aloud Rules

Read aloud must use the browser Web Speech API.

Do not introduce:
- third-party TTS services
- backend audio generation
- paid speech dependencies

Controls required:
- Read
- Pause
- Stop

---

## Continue Learning Rules

Use browser localStorage to persist the last lesson slug.

Do not introduce user accounts or server-side persistence.

---

## Search Rules

Search must remain file-based.

Search these fields:
- title
- ideas
- hook

Do not introduce Elasticsearch, Algolia, or similar services.

---

## Topic Rules

Topics are curated learning tracks and must preserve lesson order.

Agents must validate topic lesson references against the loaded lesson set.

---

## Daily Lesson Rules

Daily lesson must be deterministic for a given date.

Preferred rule:
hash(date_string) % total_lessons

If Python hash behavior is unstable across processes, use a deterministic alternative like hashlib.

---

## Development Safety Rules

Agents must not:
- restructure the repository without need
- rename key files without updating docs
- remove required schema fields
- break backward compatibility with existing lessons
- add features outside the MVP unless explicitly asked

---

## Expected Deliverables

The first complete implementation should include:
- working Flask app
- lesson loader
- topic loader
- search
- routes
- templates
- CSS
- speech.js
- sample lessons
- sample topics

---

## Decision Rule

If there is ambiguity, choose the simplest implementation that preserves:
- readability
- modularity
- deterministic behavior
- file-based content

---

## Author

Ray Austria