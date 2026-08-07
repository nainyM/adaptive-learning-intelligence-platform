"""
Adaptive difficulty logic: adjusts the learner's effective literacy_level
based on quiz performance on a topic, so future recommendations shift
easier or harder automatically.
"""

STRUGGLE_THRESHOLD = 0.5  # below this quiz-correct rate, simplify
MASTERY_THRESHOLD = 0.85  # above this, offer more advanced content


def record_quiz_result(learner, digest_id, correct: bool):
    learner["quiz_scores"][digest_id] = correct
    return learner


def topic_performance(learner, digests, topic):
    topic_digest_ids = [d["id"] for d in digests if d["topic"] == topic]
    attempted = [learner["quiz_scores"][did] for did in topic_digest_ids if did in learner["quiz_scores"]]
    if not attempted:
        return None
    return sum(1 for a in attempted if a) / len(attempted)


def adapt_literacy_level(learner, digests):
    """Look across all topics the learner has quizzed on; if they're
    struggling broadly, step literacy_level down; if mastering, step up."""
    topics = {d["topic"] for d in digests}
    rates = [topic_performance(learner, digests, t) for t in topics]
    rates = [r for r in rates if r is not None]
    if not rates:
        return learner

    avg_rate = sum(rates) / len(rates)
    levels = ["beginner", "intermediate", "advanced"]
    current_idx = levels.index(learner["literacy_level"]) if learner["literacy_level"] in levels else 0

    if avg_rate < STRUGGLE_THRESHOLD and current_idx > 0:
        learner["literacy_level"] = levels[current_idx - 1]
    elif avg_rate > MASTERY_THRESHOLD and current_idx < len(levels) - 1:
        learner["literacy_level"] = levels[current_idx + 1]

    return learner
