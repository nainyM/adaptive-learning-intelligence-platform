"""
Gamification: points for completing digests, streaks for consecutive
days of activity, and badges for topic-track milestones.
"""
from datetime import date, timedelta

POINTS_PER_DIGEST = 10
POINTS_PER_CORRECT_QUIZ = 5


def award_digest_points(learner, correct_quiz: bool):
    learner["points"] += POINTS_PER_DIGEST
    if correct_quiz:
        learner["points"] += POINTS_PER_CORRECT_QUIZ
    return learner


def log_session(learner, today: date = None):
    today = today or date.today()
    today_str = today.isoformat()
    if today_str not in learner["sessions"]:
        learner["sessions"].append(today_str)
        learner["sessions"].sort()
    return learner


def current_streak(learner, today: date = None):
    today = today or date.today()
    session_dates = {date.fromisoformat(s) for s in learner["sessions"]}
    streak = 0
    cursor = today
    while cursor in session_dates:
        streak += 1
        cursor = cursor - timedelta(days=1)
    return streak


def check_badges(learner, digests):
    topics = {d["topic"] for d in digests}
    new_badges = []
    for topic in topics:
        topic_ids = {d["id"] for d in digests if d["topic"] == topic}
        if topic_ids.issubset(set(learner["read_digests"])):
            badge = f"{topic} — Track Complete"
            if badge not in learner["badges"]:
                learner["badges"].append(badge)
                new_badges.append(badge)
    return learner, new_badges
