import psutil
from db import log_stats

def get_system_stats():
    processes = []
    for p in psutil.process_iter(attrs=["name", "cpu_percent", "memory_percent"]):
        try:
            processes.append({
                "name": p.info["name"] or "Unknown",
                "cpu": p.info["cpu_percent"],
                "memory": p.info["memory_percent"]
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    #Top 5 processes show
    processes = sorted(processes, key=lambda x: x["cpu"], reverse=True)[:10]

    stats = {
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "network": psutil.net_io_counters().bytes_sent,
        "disk": psutil.disk_usage('/').percent,
        "top_apps": processes
    }
    # Log stats to the database
    log_stats(stats)
    return stats

if __name__ == "__main__":
    import time
    import pprint
    while True:
        pprint.pprint(get_system_stats())
        time.sleep(1.5)
