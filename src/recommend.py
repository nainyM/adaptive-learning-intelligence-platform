"""
Recommendation engine: given a learner's interests, goal, literacy level,
and reading history, suggest the next-best digest.

Scoring is simple and transparent on purpose (a PM should be able to
explain exactly why something got recommended, not hide behind a black
box) -- tag overlap with stated interests, difficulty match to literacy
level, and a small penalty for already-read content.
"""


def score_digest(learner, digest):
    if digest["id"] in learner["read_digests"]:
        return -1  # already read, never recommend again

    tag_overlap = len(set(digest["tags"]) & set(learner["interests"]))
    score = tag_overlap * 10

    if digest["difficulty"] == learner["literacy_level"]:
        score += 5
    elif digest["difficulty"] == "beginner" and learner["literacy_level"] == "intermediate":
        score += 2  # still fine, just not a perfect match

    return score


def recommend_next(learner, digests, top_n=3):
    scored = [(score_digest(learner, d), d) for d in digests]
    scored = [(s, d) for s, d in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_n]]
