# SkillSnacks Architecture Decisions

## ADR-001: File-Based Content Storage
Decision:
Use JSON files stored in the repository for lessons and topics.

Reason:
- simple
- transparent
- easy to edit
- no database setup
- ideal for a lightweight MVP

---

## ADR-002: Flask Server-Rendered Application
Decision:
Use Flask with server-rendered HTML templates.

Reason:
- low complexity
- easy for learning
- fast to prototype
- fits the MVP scope

---

## ADR-003: Browser-Native Read Aloud
Decision:
Use the browser Web Speech API for read-aloud mode.

Reason:
- zero backend complexity
- no extra cost
- no audio storage
- appropriate for MVP experimentation

---

## ADR-004: Client-Side Continue Learning
Decision:
Use localStorage for continue learning.

Reason:
- avoids accounts and server persistence
- fits personal/single-user MVP
- minimal implementation effort

---

## ADR-005: Deterministic Daily Lesson
Decision:
Use deterministic daily lesson selection based on the current date.

Reason:
- predictable behavior
- same daily lesson for a given day
- easy to test