import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Mapping, Any

RESULTS_PATH = Path("data/survey.ndjson")


def sha256_hash(value: str) -> str:
    """Return the SHA-256 hash of the given string."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def append_json_line(record: Mapping[str, Any]) -> None:
    """Append a record to survey.ndjson, hashing PII and generating submission_id."""
    # --- Protect PII ---
    if "email" in record:
        record["email"] = sha256_hash(record["email"])
    if "age" in record:
        record["age"] = sha256_hash(str(record["age"]))

    # --- Add submission_id if missing ---
    if not record.get("submission_id") and "email" in record:
        now_hour = datetime.now(timezone.utc).strftime("%Y%m%d%H")
        # Use hashed email here because email is already hashed
        record["submission_id"] = sha256_hash(record["email"] + now_hour)

    # --- Ensure data folder exists ---
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    # --- Write record ---
    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                record,
                ensure_ascii=False,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else o
            ) + "\n"
        )