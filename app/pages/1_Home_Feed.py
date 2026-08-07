import os
import sys

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from src import data_store, recommend
from app.common import require_learner

st.set_page_config(page_title="Home Feed", layout="wide")
learner, learners = require_learner()
digests = data_store.load_digests()

st.title(f"Home Feed — {learner['name']}")
st.caption(f"Recommendations based on interests ({', '.join(learner['interests'])}) and literacy level ({learner['literacy_level']}).")

recs = recommend.recommend_next(learner, digests, top_n=5)

if not recs:
    st.info("No new recommendations — you've read everything matching your interests. Try updating interests or explore all digests below.")
else:
    for d in recs:
        with st.container(border=True):
            st.markdown(f"### {d['title']}")
            st.caption(f"{d['topic']} · {d['difficulty']} · tags: {', '.join(d['tags'])}")
            st.write(d["summary"])
            st.caption(f"Go to Digest Reader page and open ID **{d['id']}** to read this.")

st.markdown("---")
st.subheader("All digests")
st.dataframe(
    [{"ID": d["id"], "Title": d["title"], "Topic": d["topic"], "Difficulty": d["difficulty"],
      "Read?": "✅" if d["id"] in learner["read_digests"] else ""} for d in digests],
    use_container_width=True, hide_index=True
)
