"""养蜂场核心逻辑：蜂箱、蜜源、储蜜和病害。"""

import json

SEASONS = ("spring", "summer", "autumn", "winter")
BLOOM_SEASONS = frozenset(("spring", "summer"))
BAD_WEATHER = frozenset(("storm", "rain", "snow", "wind"))
STORAGE_CAPACITY = 1000
DISEASE_LOSS = 10
SEASON_HONEY = 5


def new_game():
    return {
        "hives": {},
        "honey": 0,
        "season": "spring",
        "batch_id": 0,
        "weather": "sunny",
        "disease_batches": [],
        "settled_batches": [],
    }


def _ensure_state(state):
    if not isinstance(state, dict):
        raise ValueError("state must be a dict")
    state.setdefault("hives", {})
    state.setdefault("honey", 0)
    state.setdefault("season", "spring")
    state.setdefault("batch_id", 0)
    state.setdefault("weather", "sunny")
    state.setdefault("disease_batches", [])
    state.setdefault("settled_batches", [])
    return state


def _positive_amount(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return value > 0


def save_state(state):
    _ensure_state(state)
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return _ensure_state(state)


def register_hive(state, hive_id):
    _ensure_state(state)
    if not isinstance(hive_id, str) or not hive_id:
        return False
    if hive_id in state["hives"]:
        return False
    state["hives"][hive_id] = {"queen": True, "population": 100}
    return True


def harvest(state, hive_id, amount):
    _ensure_state(state)
    if state["season"] not in BLOOM_SEASONS:
        return False
    hive = state["hives"].get(hive_id)
    if hive is None or not hive.get("queen", False):
        return False
    if not _positive_amount(amount):
        return False
    free = STORAGE_CAPACITY - state["honey"]
    if free <= 0:
        return False
    state["honey"] += min(amount, free)
    return True


def honey_by_weight(state):
    _ensure_state(state)
    return state["honey"]


def cancel_harvest(state, hive_id, amount):
    _ensure_state(state)
    if not _positive_amount(amount) or amount > state["honey"]:
        return False
    state["honey"] -= amount
    return True


def count_honey(state, hive_id):
    _ensure_state(state)
    hive = state["hives"].get(hive_id)
    if hive is None or not hive.get("queen", False):
        return False
    return state["honey"]


def disease(state, hive_id=None):
    _ensure_state(state)
    batch = state["batch_id"]
    if batch in state["disease_batches"]:
        return False
    if hive_id is not None:
        target = state["hives"].get(hive_id)
        if target is None:
            return False
        targets = [target]
    else:
        targets = list(state["hives"].values())
    if not targets:
        return False
    for hive in targets:
        hive["population"] = max(0, hive.get("population", 0) - DISEASE_LOSS)
    state["disease_batches"].append(batch)
    return True


def work(state):
    _ensure_state(state)
    if state.get("weather", "sunny") in BAD_WEATHER:
        return False
    if not state["hives"]:
        return False
    return True


def settle_season(state):
    _ensure_state(state)
    batch = state["batch_id"]
    if batch in state["settled_batches"]:
        return False
    gain = 0
    if state["season"] in BLOOM_SEASONS:
        gain = sum(
            SEASON_HONEY
            for hive in state["hives"].values()
            if hive.get("queen", False)
        )
    free = max(0, STORAGE_CAPACITY - state["honey"])
    state["honey"] += min(gain, free)
    state["settled_batches"].append(batch)
    return True


def advance_season(state):
    _ensure_state(state)
    settle_season(state)
    index = SEASONS.index(state["season"]) if state["season"] in SEASONS else 0
    state["season"] = SEASONS[(index + 1) % len(SEASONS)]
    state["batch_id"] += 1
    return state["batch_id"]


def main():
    print("养蜂场 - 命令: register/harvest/weight/cancel/count/disease/work/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw:
            continue
        parts = raw.split()
        command = parts[0]
        if command == "quit":
            break
        if command == "register" and len(parts) == 2:
            print("ok" if register_hive(state, parts[1]) else "no")
        elif command == "harvest" and len(parts) == 3:
            try:
                amount = int(parts[2])
            except ValueError:
                amount = -1
            print("ok" if harvest(state, parts[1], amount) else "no")
        elif command == "weight" and len(parts) == 1:
            print(honey_by_weight(state))
        elif command == "cancel" and len(parts) == 3:
            try:
                amount = int(parts[2])
            except ValueError:
                amount = -1
            print("ok" if cancel_harvest(state, parts[1], amount) else "no")
        elif command == "count" and len(parts) == 2:
            result = count_honey(state, parts[1])
            print(result if result is not False else "no")
        elif command == "disease" and len(parts) in (1, 2):
            print("ok" if disease(state, parts[1] if len(parts) == 2 else None) else "no")
        elif command == "work" and len(parts) == 1:
            print("ok" if work(state) else "no")
        else:
            print("bad command")


if __name__ == "__main__":
    main()
