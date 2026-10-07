"""Web Push (VAPID) on briefing completion — sent directly from our backend.

No third-party push vendor: the App Platform service encrypts and delivers
pushes itself via the Web Push protocol. The web UI subscribes through its
service worker (web/sw.js).
"""
import json
import os

from ..memory.store import list_subscriptions


def _vapid():
    return {
        "private_key": os.getenv("VAPID_PRIVATE_KEY", ""),
        "public_key": os.getenv("VAPID_PUBLIC_KEY", ""),
        "claims_sub": os.getenv("VAPID_SUBJECT", "mailto:sidekick@example.com"),
    }


async def push_briefing_ready(topic: str, briefing_id: int) -> int:
    """Push to all subscribed devices. Returns number of pushes sent."""
    v = _vapid()
    subs = await list_subscriptions()
    if not v["private_key"] or not subs:
        return 0
    from pywebpush import WebPushException, webpush

    payload = json.dumps({"title": "Sidekick",
                          "body": f"Your briefing is ready: {topic}",
                          "briefing_id": briefing_id})
    sent = 0
    for s in subs:
        try:
            webpush(
                subscription_info={"endpoint": s["endpoint"],
                                   "keys": {"p256dh": s["p256dh"], "auth": s["auth"]}},
                data=payload,
                vapid_private_key=v["private_key"],
                vapid_claims={"sub": v["claims_sub"]},
            )
            sent += 1
        except WebPushException:
            continue  # expired subscription; leave cleanup for later
    return sent
