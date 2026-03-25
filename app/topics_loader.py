from __future__ import annotations

import json
from pathlib import Path


REQUIRED_TOPIC_FIELDS = {"topic_id", "title", "description", "lessons"}


def load_topics(topics_dir: str | Path, lesson_index: dict[str, dict]) -> list[dict]:
    topics_path = Path(topics_dir)
    topics: list[dict] = []

    for file_path in sorted(topics_path.glob("*.json")):
        with file_path.open("r", encoding="utf-8") as handle:
            topic = json.load(handle)

        missing_fields = REQUIRED_TOPIC_FIELDS - topic.keys()
        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(f"Topic file {file_path.name} is missing required fields: {missing}")

        ordered_lessons = []
        missing_lessons = []
        for slug in topic["lessons"]:
            lesson = lesson_index.get(slug)
            if lesson is None:
                missing_lessons.append(slug)
                continue
            ordered_lessons.append(lesson)

        topic["ordered_lessons"] = ordered_lessons
        topic["missing_lessons"] = missing_lessons
        topics.append(topic)

    return sorted(topics, key=lambda topic: topic["title"])


def build_topic_index(topics: list[dict]) -> dict[str, dict]:
    return {topic["topic_id"]: topic for topic in topics}
