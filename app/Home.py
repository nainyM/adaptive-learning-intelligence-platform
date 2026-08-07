import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, gamification
from app import mascot

st.set_page_config(page_title="Health Literacy — Adaptive Learning", layout="wide")

mascot.render("idle")
st.title("Adaptive Learning Intelligence Platform")
st.caption("A mock health-literacy EdTech product — personalized digests, adaptive difficulty, gamification, and a RAG learning copilot. All data is simulated.")

learners = data_store.load_learners()

st.subheader("Select a learner profile (mock login)")
names = {l["id"]: f"{l['name']} — goal: {l['goal']}" for l in learners}
choice = st.radio("Choose a profile:", list(names.keys()), format_func=lambda k: names[k])

if st.button("Log in", type="primary"):
    st.session_state["learner_id"] = choice
    learner = data_store.get_learner(learners, choice)
    learner = gamification.log_session(learner)
    data_store.update_learner(learners, learner)
    st.success(f"Logged in as {learner['name']}. Use the sidebar to navigate: Home Feed, Digest Reader, Gamification, Copilot, Measurement Dashboard.")

if "learner_id" in st.session_state:
    learner = data_store.get_learner(learners, st.session_state["learner_id"])
    st.markdown("---")
    st.markdown(f"**Currently logged in as:** {learner['name']}")
    st.markdown(f"**Literacy level:** {learner['literacy_level']}")
    st.markdown(f"**Interests:** {', '.join(learner['interests'])}")
