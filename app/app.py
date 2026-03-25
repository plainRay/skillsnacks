from __future__ import annotations

import hashlib
import random
from datetime import date
from pathlib import Path

from flask import Flask, abort, redirect, render_template, request, send_from_directory, url_for

if __package__:
    from .lesson_loader import (
        build_lesson_index,
        get_adjacent_lessons,
        get_categories,
        group_lessons_by_category,
        load_lessons,
    )
    from .progress_manager import build_topic_groups, build_topic_progress_data, get_lesson_position
    from .search_engine import search_lessons
    from .streak_manager import get_today_string
    from .topics_loader import build_topic_index, load_topics
else:
    from lesson_loader import (
        build_lesson_index,
        get_adjacent_lessons,
        get_categories,
        group_lessons_by_category,
        load_lessons,
    )
    from progress_manager import build_topic_groups, build_topic_progress_data, get_lesson_position
    from search_engine import search_lessons
    from streak_manager import get_today_string
    from topics_loader import build_topic_index, load_topics


BASE_DIR = Path(__file__).resolve().parent.parent
LESSONS_DIR = BASE_DIR / "lessons"
TOPICS_DIR = BASE_DIR / "topics"
STATIC_DIR = BASE_DIR / "static"
STATIC_AUDIO_DIR = STATIC_DIR / "audio"
PWA_DIR = STATIC_DIR / "pwa"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)


def build_app_state() -> dict:
    lessons = load_lessons(LESSONS_DIR)
    lesson_index = build_lesson_index(lessons)
    lessons_by_category = group_lessons_by_category(lessons)
    categories = get_categories(lessons_by_category)
    topics = load_topics(TOPICS_DIR, lesson_index)
    topic_index = build_topic_index(topics)
    topic_progress = build_topic_progress_data(topics)
    topic_groups = build_topic_groups(topics)

    return {
        "lessons": lessons,
        "lesson_index": lesson_index,
        "lessons_by_category": lessons_by_category,
        "categories": categories,
        "topics": topics,
        "topic_index": topic_index,
        "topic_progress": topic_progress,
        "topic_groups": topic_groups,
    }


STATE = build_app_state()


def get_daily_lesson(current_date: date | None = None) -> dict | None:
    lessons = STATE["lessons"]
    if not lessons:
        return None

    selected_date = current_date or date.today()
    date_string = selected_date.isoformat()
    digest = hashlib.sha256(date_string.encode("utf-8")).hexdigest()
    lesson_index = int(digest, 16) % len(lessons)
    return lessons[lesson_index]


def resolve_next_lessons(lesson_data: dict) -> list[dict]:
    next_lessons = []
    for slug in lesson_data.get("next_lessons", []):
        linked_lesson = STATE["lesson_index"].get(slug)
        if linked_lesson is not None:
            next_lessons.append(linked_lesson)
    return next_lessons


def get_audio_url(slug: str) -> str | None:
    audio_file = STATIC_AUDIO_DIR / f"{slug}.mp3"
    if audio_file.exists():
        return url_for("static", filename=f"audio/{slug}.mp3")
    return None


@app.context_processor
def inject_site_data() -> dict:
    return {
        "site_name": "SkillSnacks",
        "global_search_placeholder": "🔍 Search ideas, hooks, titles",
        "global_today_string": get_today_string(),
    }


@app.route("/")
def home():
    lessons = STATE["lessons"]
    featured_lesson = lessons[0] if lessons else None
    daily_lesson = get_daily_lesson()
    recent_lessons = lessons[:6]
    return render_template(
        "home.html",
        daily_lesson=daily_lesson,
        lesson_cards=recent_lessons,
        topics=STATE["topics"],
        topic_groups=STATE["topic_groups"],
        today_string=get_today_string(),
    )


@app.route("/category/<category_name>")
def category(category_name: str):
    lessons = STATE["lessons_by_category"].get(category_name, [])
    status_code = 200 if lessons else 404
    return (
        render_template(
            "category.html",
            category_name=category_name,
            category_title=category_name.replace("-", " ").title(),
            lessons=lessons,
        ),
        status_code,
    )


@app.route("/lesson/<slug>")
def lesson(slug: str):
    lesson_data = STATE["lesson_index"].get(slug)
    if lesson_data is None:
        abort(404)

    previous_lesson, next_lesson = get_adjacent_lessons(STATE["lessons"], slug)
    lesson_position = get_lesson_position(STATE["lessons"], slug)
    return render_template(
        "lesson.html",
        lesson=lesson_data,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        next_lesson_cards=resolve_next_lessons(lesson_data),
        audio_url=get_audio_url(slug),
        lesson_position=lesson_position,
        page_label=None,
        today_string=get_today_string(),
    )


@app.route("/topics")
def topics():
    return render_template(
        "topics.html",
        topics=STATE["topics"],
        topic_progress=STATE["topic_progress"],
        topic_groups=STATE["topic_groups"],
    )


@app.route("/topic/<topic_id>")
def topic(topic_id: str):
    topic_data = STATE["topic_index"].get(topic_id)
    if topic_data is None:
        abort(404)

    return render_template("topic.html", topic=topic_data)


@app.route("/daily")
def daily():
    daily_lesson = get_daily_lesson()
    if daily_lesson is None:
        abort(404)

    previous_lesson, next_lesson = get_adjacent_lessons(STATE["lessons"], daily_lesson["slug"])
    lesson_position = get_lesson_position(STATE["lessons"], daily_lesson["slug"])
    return render_template(
        "lesson.html",
        lesson=daily_lesson,
        previous_lesson=previous_lesson,
        next_lesson=next_lesson,
        next_lesson_cards=resolve_next_lessons(daily_lesson),
        audio_url=get_audio_url(daily_lesson["slug"]),
        lesson_position=lesson_position,
        page_label=f"Daily Curiosity for {date.today().isoformat()}",
        today_string=get_today_string(),
    )


@app.route("/random")
def random_lesson():
    lessons = STATE["lessons"]
    if not lessons:
        abort(404)

    lesson_data = random.choice(lessons)
    return redirect(url_for("lesson", slug=lesson_data["slug"]))


@app.route("/surprise")
def surprise():
    return random_lesson()


@app.route("/search")
def search():
    query = request.args.get("q", "")
    results = search_lessons(STATE["lessons"], query)
    return render_template("search.html", query=query, results=results)


@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(PWA_DIR, "service-worker.js")


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
