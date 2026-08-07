"""
Measurement loop: mastery, engagement, completion, and recommendation
effectiveness -- same conceptual shape as the L4 Business Outcome layer
in the eval framework project, adapted to a learning product.
"""
from .gamification import current_streak


def mastery_score(learner):
    if not learner["quiz_scores"]:
        return None
    correct = sum(1 for v in learner["quiz_scores"].values() if v)
    return round(correct / len(learner["quiz_scores"]) * 100, 1)


def engagement_score(learner):
    return {
        "total_sessions": len(learner["sessions"]),
        "current_streak": current_streak(learner),
    }


def completion_rate(learner, digests):
    total = len(digests)
    if total == 0:
        return 0
    return round(len(learner["read_digests"]) / total * 100, 1)


def recommendation_effectiveness(learner, recommended_ids_ever, read_ids):
    """% of everything ever recommended that was actually opened/read."""
    if not recommended_ids_ever:
        return None
    opened = len(set(recommended_ids_ever) & set(read_ids))
    return round(opened / len(recommended_ids_ever) * 100, 1)
