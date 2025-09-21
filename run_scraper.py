import asyncio
from monitor.config import SCHEDULER
from monitor.main import run_once, run_daemon

if __name__ == "__main__":
    if SCHEDULER:
        asyncio.run(run_daemon())
    else:
        asyncio.run(run_once())
