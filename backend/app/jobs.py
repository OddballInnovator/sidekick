"""In-process scheduler (APScheduler). App Platform jobs are the production path."""
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .agent.research import run_research_job
from .memory.store import save_job

scheduler = AsyncIOScheduler()


def schedule_job(topic: str, run_at: str | None) -> dict:
    """run_at: ISO datetime. None -> run in 60s (demo default)."""
    import datetime
    when = datetime.datetime.fromisoformat(run_at) if run_at else (
        datetime.datetime.now() + datetime.timedelta(seconds=60))
    job = scheduler.add_job(run_research_job, "date", run_date=when,
                            kwargs={"topic": topic})
    return {"scheduler_job_id": job.id, "topic": topic, "run_at": when.isoformat()}
