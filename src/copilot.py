"""
Mock RAG-style learning copilot. Retrieval: simple keyword overlap
against the digest library (standing in for real vector search). The
"generation" step is templated rather than a real LLM call, matching
the same mock-first pattern used in the eval framework project.

Guardrail: every answer includes a fixed disclaimer -- this is a health
LITERACY copilot, not a source of diagnosis or personalized medical advice.
"""

DISCLAIMER = (
    "This explains general health science for learning purposes only — "
    "it isn't medical advice. Talk to a doctor about your specific situation."
)


def retrieve(query: str, digests: list, top_n: int = 2):
    query_words = set(query.lower().split())
    scored = []
    for d in digests:
        content_words = set((d["title"] + " " + d["summary"] + " " + d["body"]).lower().split())
        overlap = len(query_words & content_words)
        if overlap > 0:
            scored.append((overlap, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_n]]


def answer(query: str, digests: list):
    matches = retrieve(query, digests)
    if not matches:
        return {
            "answer": "I don't have a digest covering that yet — try asking about sleep, nutrition, heart health, stress, exercise, or gut health.",
            "sources": [],
            "disclaimer": DISCLAIMER,
        }

    top = matches[0]
    generated = f"Based on \"{top['title']}\": {top['summary']} {top['body'][:220]}..."
    return {
        "answer": generated,
        "sources": [m["title"] for m in matches],
        "disclaimer": DISCLAIMER,
    }
