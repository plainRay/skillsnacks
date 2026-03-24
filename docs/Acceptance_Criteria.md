# SkillSnacks Acceptance Criteria

## MVP Acceptance Criteria

### Application Boot
- Flask app starts successfully with `python app/app.py`
- No required database setup
- App loads at http://127.0.0.1:5000

### Home Page
- Home page renders without errors
- Displays site title
- Displays categories
- Displays topics
- Displays daily lesson section
- Displays lesson cards
- Displays continue learning card if last lesson exists

### Lessons
- Lesson pages render without errors
- Each lesson shows:
  - title
  - category
  - reading time
  - why section
  - ideas list
  - curiosity hook
- Previous and next lesson links work

### Categories
- Category page shows all lessons for the category
- Category page handles unknown category gracefully

### Topics
- Topics index page shows all topics
- Topic page shows ordered lesson list
- Invalid lesson references in topics do not crash the app

### Search
- Search returns relevant lessons for matching keywords
- Search supports title, ideas, and hook fields
- Empty or no-match queries are handled gracefully

### Daily Curiosity
- Daily lesson is deterministic for the same day
- Daily lesson changes across different days

### Random Discovery
- Random route redirects to a valid lesson

### Continue Learning
- Visiting a lesson stores its slug in localStorage
- Home page can read and display the last lesson link

### Read Aloud
- Read button starts speech synthesis
- Pause button pauses speech
- Stop button cancels speech
- Feature is implemented with browser-native APIs only

### UI / UX
- Layout is readable on desktop and mobile widths
- Lesson cards are visually distinct
- Navigation is clear
- Content remains the primary focus

### Code Quality
- Code is modular
- No unnecessary frameworks
- No database added
- No server-side speech service added