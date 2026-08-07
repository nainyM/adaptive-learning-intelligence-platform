"""
Mock notification generator -- produces notification-worthy events based
on learner state. In a real product these would be pushed (email/push
notification); here they're just generated as a list for the UI to show,
since there's no real notification delivery channel connected.
"""


def generate_notifications(learner, recommendations, streak: int, new_badges: list):
    notes = []

    if streak >= 3:
        notes.append(f"You're on a {streak}-day streak. Keep it going!")

    if not learner["sessions"]:
        notes.append("Welcome! Start with a digest matched to your goal.")

    if recommendations:
        top = recommendations[0]
        notes.append(f"New digest matched to your interests: \"{top['title']}\"")

    for badge in new_badges:
        notes.append(f"Badge earned: {badge}")

    if len(learner["sessions"]) >= 1 and streak == 0:
        notes.append("You haven't checked in recently — pick up where you left off.")

    return notes
