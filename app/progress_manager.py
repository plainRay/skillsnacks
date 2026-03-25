from __future__ import annotations


def get_lesson_position(lessons: list[dict], slug: str) -> dict[str, int] | None:
    total = len(lessons)
    for index, lesson in enumerate(lessons, start=1):
        if lesson["slug"] == slug:
            return {"current": index, "total": total}

    return None


def build_topic_progress_data(topics: list[dict]) -> list[dict]:
    topic_progress = []
    for topic in topics:
        topic_progress.append(
            {
                "topic_id": topic["topic_id"],
                "title": topic["title"],
                "lesson_slugs": [lesson["slug"] for lesson in topic.get("ordered_lessons", [])],
                "total_lessons": len(topic.get("ordered_lessons", [])),
            }
        )

    return topic_progress


def build_topic_groups(topics: list[dict]) -> list[dict]:
    domain_labels = {
        "medical": "Medicine",
        "medicine": "Medicine",
        "science": "Science",
        "history": "History",
        "technology": "Technology",
        "culture": "Culture",
        "psychology": "Psychology",
        "space": "Space",
    }

    grouped: dict[str, list[dict]] = {}
    for topic in topics:
        if topic.get("ordered_lessons"):
            category = topic["ordered_lessons"][0]["category"]
            domain = domain_labels.get(category, category.replace("-", " ").title())
        else:
            domain = "General"

        grouped.setdefault(domain, []).append(topic)

    return [
        {"domain": domain, "topics": sorted(grouped_topics, key=lambda topic: topic["title"])}
        for domain, grouped_topics in sorted(grouped.items())
    ]
