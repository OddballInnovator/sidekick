"""Model resolution: direct model, or the Inference Router when configured.

Set DO_INFERENCE_ROUTER to a router name (created in console: Inference >
Routers, e.g. cost-efficiency preset) and every call goes through
"router:<name>" — the router classifies each request and picks the best
model per dollar. Unset -> DO_INFERENCE_MODEL directly.
"""
import os


def resolve_model() -> str:
    router = os.getenv("DO_INFERENCE_ROUTER", "").strip()
    if router:
        return f"router:{router}"
    return os.getenv("DO_INFERENCE_MODEL", "openai/gpt-5-mini")
