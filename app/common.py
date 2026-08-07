"""Shared setup for every page: puts the project root on sys.path so
`from src import ...` works no matter which page Streamlit runs, and
holds the mock "login" (learner selection) in session_state."""
import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store


def require_learner():
    """Returns the selected learner dict, or stops the page with a
    prompt to go back to Home and log in if none is selected yet."""
    if "learner_id" not in st.session_state:
        st.warning("Please select a learner profile on the Home page first.")
        st.stop()
    learners = data_store.load_learners()
    learner = data_store.get_learner(learners, st.session_state["learner_id"])
    return learner, learners
