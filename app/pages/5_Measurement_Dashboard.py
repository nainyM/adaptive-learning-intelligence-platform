import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, measurement
from app.common import require_learner

st.set_page_config(page_title="Measurement Dashboard", layout="wide")
learner, learners = require_learner()
digests = data_store.load_digests()

st.title(f"Measurement Loop — {learner['name']}")
st.caption("Mastery, engagement, completion, and recommendation effectiveness — the same measurement-loop pattern as the multi-judge-eval-framework project, applied to a learning product.")

mastery = measurement.mastery_score(learner)
engagement = measurement.engagement_score(learner)
completion = measurement.completion_rate(learner, digests)

col1, col2, col3 = st.columns(3)
col1.metric("Mastery (quiz accuracy)", f"{mastery}%" if mastery is not None else "No quizzes yet")
col2.metric("Sessions", engagement["total_sessions"])
col3.metric("Completion rate", f"{completion}%")

st.markdown("---")
st.subheader("All learners (comparison view)")
rows = []
for l in learners:
    m = measurement.mastery_score(l)
    e = measurement.engagement_score(l)
    c = measurement.completion_rate(l, digests)
    rows.append({
        "Learner": l["name"],
        "Literacy Level": l["literacy_level"],
        "Mastery": f"{m}%" if m is not None else "—",
        "Sessions": e["total_sessions"],
        "Streak": e["current_streak"],
        "Completion": f"{c}%",
        "Points": l["points"],
        "Badges": len(l["badges"]),
    })
st.dataframe(rows, use_container_width=True, hide_index=True)
