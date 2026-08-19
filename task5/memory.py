import json
import pathlib

STORE = pathlib.Path("memory.json")


def _load() -> dict:
    return json.loads(STORE.read_text()) if STORE.exists() else {}


def remember(key: str, value: str) -> str:
    data = _load()
    data[key] = value
    STORE.write_text(json.dumps(data, indent=2))
    return f"stored {key}"


def recall(key: str) -> str:
    return _load().get(key, "not found")


def snapshot(run_id: str, history: list) -> None:
    pathlib.Path("traces").mkdir(exist_ok=True)
    pathlib.Path(f"traces/run_{run_id}.json").write_text(
        json.dumps(history, indent=2)
    )