from __future__ import annotations


def search_lessons(lessons: list[dict], query: str) -> list[dict]:
    normalized_query = query.strip().lower()
    if not normalized_query:
        return []

    matches = []
    for lesson in lessons:
        searchable_text = " ".join(
            [
                lesson["title"],
                lesson.get("puzzle", ""),
                lesson.get("insight", ""),
                " ".join(lesson.get("key_ideas", lesson.get("ideas", []))),
                lesson.get("mind_blower", lesson.get("hook", "")),
                lesson.get("next_curiosity", ""),
            ]
        ).lower()

        if normalized_query in searchable_text:
            matches.append(lesson)

    return matches
