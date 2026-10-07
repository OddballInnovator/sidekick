"""OneSignal push on briefing completion. No-op without keys."""
import os

import httpx

ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID", "")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY", "")


async def push_briefing_ready(topic: str, briefing_id: int) -> None:
    if not (ONESIGNAL_APP_ID and ONESIGNAL_API_KEY):
        return  # not configured; the briefing view is the fallback surface
    async with httpx.AsyncClient(timeout=30) as client:
        await client.post(
            "https://onesignal.com/api/v1/notifications",
            headers={"Authorization": f"Basic {ONESIGNAL_API_KEY}"},
            json={
                "app_id": ONESIGNAL_APP_ID,
                "included_segments": ["All"],
                "headings": {"en": "Sidekick"},
                "contents": {"en": f"Your briefing is ready: {topic}"},
                "data": {"briefing_id": briefing_id},
            },
        )
