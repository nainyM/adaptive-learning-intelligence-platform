import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, copilot
from app.common import require_learner

st.set_page_config(page_title="Learning Copilot", layout="wide")
learner, learners = require_learner()
digests = data_store.load_digests()

st.title("Health Learning Copilot")
st.caption(
    "Ask a question about topics in the digest library (sleep, nutrition, heart health, "
    "stress, exercise, gut health). Mock retrieval + templated response — not a real LLM call."
)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

query = st.text_input("Ask a question")
if st.button("Ask", type="primary") and query:
    result = copilot.answer(query, digests)
    st.session_state["chat_history"].append((query, result))

for q, r in reversed(st.session_state["chat_history"]):
    with st.container(border=True):
        st.markdown(f"**You:** {q}")
        st.markdown(f"**Copilot:** {r['answer']}")
        if r["sources"]:
            st.caption(f"Sources: {', '.join(r['sources'])}")
        st.caption(r["disclaimer"])
