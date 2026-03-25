from __future__ import annotations

import json
from pathlib import Path


REQUIRED_LESSON_FIELDS = {"slug", "title"}


def normalize_lesson(lesson: dict, file_name: str) -> dict:
    missing_fields = REQUIRED_LESSON_FIELDS - lesson.keys()
    if missing_fields:
        missing = ", ".join(sorted(missing_fields))
        raise ValueError(f"Lesson file {file_name} is missing required fields: {missing}")

    topic = lesson.get("topic") or lesson.get("category")
    category = lesson.get("category") or topic
    if not category:
        path = Path(file_name)
        if len(path.parts) > 1:
            category = path.parts[0]
        else:
            raise ValueError(f"Lesson file {file_name} must include category or live inside a category folder")
    topic = topic or category

    reading_time = lesson.get("reading_time") or lesson.get("time")
    if not reading_time:
        raise ValueError(f"Lesson file {file_name} must include reading_time or time")

    key_ideas = lesson.get("key_ideas") or lesson.get("ideas")
    if not isinstance(key_ideas, list) or not key_ideas:
        raise ValueError(f"Lesson file {file_name} must include key_ideas or ideas as a non-empty list")

    puzzle = lesson.get("puzzle") or lesson.get("why")
    insight = lesson.get("insight") or lesson.get("why")
    mind_blower = lesson.get("mind_blower") or lesson.get("hook")
    next_curiosity = lesson.get("next_curiosity") or lesson.get("hook")

    if not all([puzzle, insight, mind_blower, next_curiosity]):
        raise ValueError(
            f"Lesson file {file_name} must include puzzle/insight/mind_blower/next_curiosity or legacy why/hook fields"
        )

    lesson["reading_time"] = reading_time
    lesson["time"] = reading_time
    lesson["topic"] = topic
    lesson["category"] = category
    lesson["puzzle"] = puzzle
    lesson["insight"] = insight
    lesson["why"] = insight
    lesson["key_ideas"] = key_ideas
    lesson["ideas"] = key_ideas
    lesson["mind_blower"] = mind_blower
    lesson["hook"] = mind_blower
    lesson["next_curiosity"] = next_curiosity
    lesson["next_lessons"] = lesson.get("next_lessons", [])
    lesson["narration_text"] = lesson.get("narration_text") or " ".join(
        [lesson["title"], puzzle, insight, *key_ideas, mind_blower, next_curiosity]
    )
    lesson["summary"] = insight
    lesson.setdefault("topics", [])
    lesson.setdefault("learn_more", [])
    return lesson


def load_lessons(lessons_dir: str | Path) -> list[dict]:
    lessons_path = Path(lessons_dir)
    lessons: list[dict] = []

    for file_path in sorted(lessons_path.rglob("*.json")):
        with file_path.open("r", encoding="utf-8") as handle:
            lesson = json.load(handle)

        lessons.append(normalize_lesson(lesson, str(file_path.relative_to(lessons_path))))

    return sorted(lessons, key=lambda lesson: (lesson["category"], lesson["title"]))


def build_lesson_index(lessons: list[dict]) -> dict[str, dict]:
    return {lesson["slug"]: lesson for lesson in lessons}


def group_lessons_by_category(lessons: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for lesson in lessons:
        grouped.setdefault(lesson["category"], []).append(lesson)

    return {category: grouped[category] for category in sorted(grouped)}


def get_categories(lessons_by_category: dict[str, list[dict]]) -> list[dict]:
    categories = []
    for category, lessons in lessons_by_category.items():
        categories.append(
            {
                "slug": category,
                "title": category.replace("-", " ").title(),
                "count": len(lessons),
            }
        )

    return categories


def get_adjacent_lessons(lessons: list[dict], slug: str) -> tuple[dict | None, dict | None]:
    for index, lesson in enumerate(lessons):
        if lesson["slug"] != slug:
            continue

        previous_lesson = lessons[index - 1] if index > 0 else None
        next_lesson = lessons[index + 1] if index < len(lessons) - 1 else None
        return previous_lesson, next_lesson

    return None, None
