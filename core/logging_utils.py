from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

class EventLogger:
    def __init__(self, jsonl_path: str):
        self.path = Path(jsonl_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, event: str, data: Optional[Dict[str, Any]] = None):
        rec = {
            "ts": time.time(),
            "event": event,
            "data": data or {},
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
