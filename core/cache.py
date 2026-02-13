from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Optional

def _hash_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

class SimpleCache:
    def __init__(self, base_dir: str = ".lexrecon_cache"):
        self.base = Path(base_dir)
        self.base.mkdir(parents=True, exist_ok=True)

    def key_path(self, key: str) -> Path:
        return self.base / (key + ".json")

    def make_key(self, name: str, params: dict) -> str:
        payload = json.dumps({"name": name, "params": params}, sort_keys=True)
        return _hash_str(payload)

    def get(self, key: str) -> Optional[dict]:
        p = self.key_path(key)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None

    def set(self, key: str, value: dict) -> None:
        p = self.key_path(key)
        p.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
