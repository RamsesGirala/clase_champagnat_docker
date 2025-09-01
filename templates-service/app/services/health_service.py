from pymongo.database import Database
from pymongo.errors import PyMongoError

class HealthService:
    def __init__(self, db: Database, min_available_mb: int = 100):
        self.db = db
        self.min_available_mb = min_available_mb

    def is_mongo_healthy(self) -> bool:
        try:
            self.db.command("ping")
            return True
        except PyMongoError:
            return False

    def get_available_memory(self) -> int:
        with open("/proc/meminfo", "r") as f:
            meminfo = f.readlines()
        mem_available = next(
            int(line.split()[1]) for line in meminfo if "MemAvailable" in line
        )
        return mem_available // 1024  # Convertir a MB

    def is_memory_ok(self) -> bool:
        available_mb = self.get_available_memory()
        return True

    def is_ready(self) -> bool:
        return self.is_mongo_healthy() and self.is_memory_ok()

    def is_alive(self) -> bool:
        return True
