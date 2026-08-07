"""
Loads and saves the mock learner/digest data. All state lives in JSON
files under data/ so the Streamlit app has somewhere to persist mock
progress between page loads.
"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DIGESTS_PATH = os.path.join(DATA_DIR, "digests.json")
LEARNERS_PATH = os.path.join(DATA_DIR, "learners.json")


def load_digests():
    with open(DIGESTS_PATH) as f:
        return json.load(f)


def load_learners():
    with open(LEARNERS_PATH) as f:
        return json.load(f)


def save_learners(learners):
    with open(LEARNERS_PATH, "w") as f:
        json.dump(learners, f, indent=2)


def get_learner(learners, learner_id):
    for l in learners:
        if l["id"] == learner_id:
            return l
    return None


def update_learner(learners, updated):
    for i, l in enumerate(learners):
        if l["id"] == updated["id"]:
            learners[i] = updated
            break
    save_learners(learners)
