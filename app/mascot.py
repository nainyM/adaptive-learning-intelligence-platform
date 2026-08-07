"""
A small reusable cartoon "learning buddy" blob character, rendered as
inline SVG + CSS animation. No dialogue/speech bubbles -- purely
animated reactions, driven by a `state` parameter:

  idle      - gentle bobbing, used on Home/Feed pages
  celebrate - bigger bounce + spin, used on correct answers / badges
  encourage - a soft side-to-side wiggle, used on incorrect answers
"""
import textwrap

import streamlit as st

_ANIMATIONS = {
    "idle": "buddy-bob 2.4s ease-in-out infinite",
    "celebrate": "buddy-celebrate 0.9s ease-in-out",
    "encourage": "buddy-wiggle 0.6s ease-in-out",
}

_CSS = """
<style>
@keyframes buddy-bob {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(-3deg); }
}
@keyframes buddy-celebrate {
    0% { transform: scale(1) rotate(0deg); }
    25% { transform: scale(1.15) rotate(-8deg); }
    50% { transform: scale(1.25) rotate(8deg); }
    75% { transform: scale(1.15) rotate(-4deg); }
    100% { transform: scale(1) rotate(0deg); }
}
@keyframes buddy-wiggle {
    0%, 100% { transform: translateX(0) rotate(0deg); }
    25% { transform: translateX(-6px) rotate(-4deg); }
    75% { transform: translateX(6px) rotate(4deg); }
}
.buddy-wrap {
    display: flex;
    justify-content: center;
    padding: 8px 0 4px 0;
}
</style>
"""


def _eyes(state):
    if state == "celebrate":
        # happy closed/curved eyes
        return (
            '<path d="M42 58 Q48 50 54 58" stroke="#1F2937" stroke-width="4" '
            'fill="none" stroke-linecap="round"/>'
            '<path d="M76 58 Q82 50 88 58" stroke="#1F2937" stroke-width="4" '
            'fill="none" stroke-linecap="round"/>'
        )
    if state == "encourage":
        return (
            '<circle cx="48" cy="58" r="5" fill="#1F2937"/>'
            '<circle cx="82" cy="58" r="5" fill="#1F2937"/>'
        )
    return (
        '<circle cx="48" cy="58" r="6" fill="#1F2937"/>'
        '<circle cx="82" cy="58" r="6" fill="#1F2937"/>'
    )


def _mouth(state):
    if state == "celebrate":
        return '<path d="M50 78 Q65 96 80 78" stroke="#1F2937" stroke-width="4" fill="none" stroke-linecap="round"/>'
    if state == "encourage":
        return '<path d="M52 82 Q65 76 78 82" stroke="#1F2937" stroke-width="4" fill="none" stroke-linecap="round"/>'
    return '<path d="M52 78 Q65 88 78 78" stroke="#1F2937" stroke-width="4" fill="none" stroke-linecap="round"/>'


def render(state: str = "idle", size: int = 110):
    anim = _ANIMATIONS.get(state, _ANIMATIONS["idle"])
    parts = [
        _CSS,
        '<div class="buddy-wrap">',
        f'<svg width="{size}" height="{size}" viewBox="0 0 130 130" '
        f'style="animation: {anim};" role="img" aria-label="Learning buddy character">',
        '<ellipse cx="65" cy="70" rx="55" ry="50" fill="#7CC6D6"/>',
        '<ellipse cx="65" cy="70" rx="55" ry="50" fill="none" stroke="#4C93A3" stroke-width="3"/>',
        '<circle cx="30" cy="35" r="8" fill="#7CC6D6" stroke="#4C93A3" stroke-width="3"/>',
        '<circle cx="100" cy="35" r="8" fill="#7CC6D6" stroke="#4C93A3" stroke-width="3"/>',
        _eyes(state),
        _mouth(state),
        '</svg>',
        '</div>',
    ]
    svg = "".join(parts)
    st.markdown(svg, unsafe_allow_html=True)
