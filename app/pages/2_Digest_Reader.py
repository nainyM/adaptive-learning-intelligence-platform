import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, adaptive, gamification
from app.common import require_learner

st.set_page_config(page_title="Digest Reader", layout="wide")
learner, learners = require_learner()
digests = data_store.load_digests()

st.title("Digest Reader")

digest_ids = [d["id"] for d in digests]
selected_id = st.selectbox(
    "Choose a digest to read",
    digest_ids,
    format_func=lambda did: next(d["title"] for d in digests if d["id"] == did),
)
digest = next(d for d in digests if d["id"] == selected_id)

st.subheader(digest["title"])
st.caption(f"{digest['topic']} · {digest['difficulty']}")
st.write(digest["body"])

st.markdown("---")
st.markdown(f"**Quick check:** {digest['quiz']['question']}")
user_answer = st.text_input("Your answer")

if st.button("Submit answer", type="primary"):
    correct = user_answer.strip().lower() in digest["quiz"]["answer"].lower() or digest["quiz"]["answer"].lower() in user_answer.strip().lower()

    if digest["id"] not in learner["read_digests"]:
        learner["read_digests"].append(digest["id"])

    learner = adaptive.record_quiz_result(learner, digest["id"], correct)
    learner = adaptive.adapt_literacy_level(learner, digests)
    learner = gamification.award_digest_points(learner, correct)
    learner, new_badges = gamification.check_badges(learner, digests)

    data_store.update_learner(learners, learner)

    if correct:
        st.success(f"Correct! Answer: {digest['quiz']['answer']}. +15 points.")
    else:
        st.warning(f"Not quite — the answer was: {digest['quiz']['answer']}. +10 points for reading.")

    st.info(f"Literacy level is now: **{learner['literacy_level']}** (adjusts automatically based on quiz performance).")

    for b in new_badges:
        st.balloons()
        st.success(f"Badge earned: {b}")
