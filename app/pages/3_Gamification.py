import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, gamification, notifications, recommend
from app.common import require_learner
from app import mascot

st.set_page_config(page_title="Gamification & Notifications", layout="wide")
learner, learners = require_learner()
digests = data_store.load_digests()

streak = gamification.current_streak(learner)
mascot.render("celebrate" if streak >= 3 or learner["badges"] else "idle", size=90)
st.title(f"Progress — {learner['name']}")
col1, col2, col3 = st.columns(3)
col1.metric("Points", learner["points"])
col2.metric("Current streak (days)", streak)
col3.metric("Digests read", f"{len(learner['read_digests'])} / {len(digests)}")

st.markdown("---")
st.subheader("Badges")
if learner["badges"]:
    for b in learner["badges"]:
        st.markdown(f"🏅 {b}")
else:
    st.caption("No badges yet — complete every digest in a topic track to earn one.")

st.markdown("---")
st.subheader("Notifications")
recs = recommend.recommend_next(learner, digests, top_n=1)
notes = notifications.generate_notifications(learner, recs, streak, [])
if notes:
    for n in notes:
        st.info(n)
else:
    st.caption("No notifications right now.")
