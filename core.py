"""养蜂场核心逻辑：蜂箱、蜜源、储蜜和病害。"""

import json

BLOOM_SEASONS = ("spring", "summer", "autumn")
BAD_WEATHER = ("storm", "rain", "snow")
MAX_HONEY = 1000


def new_game():
    return {
        "hives": {},
        "honey": 0,
        "season": "spring",
        "batch_id": 0,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    if text is None or not str(text).strip():
        raise ValueError("存档数据为空")
    state = json.loads(text)
    if not isinstance(state, dict):
        raise ValueError("存档格式非法")
    merged = new_game()
    merged.update(state)
    if not isinstance(merged["hives"], dict):
        raise ValueError("蜂箱数据非法")
    return merged


def register_hive(state, hive_id):
    if not hive_id or not str(hive_id).strip():
        return False
    if hive_id in state["hives"]:
        return False
    state["hives"][hive_id] = {"queen": True, "population": 100}
    return True


def harvest(state, hive_id, amount):
    if state.get("season") not in BLOOM_SEASONS:
        return False
    hive = state["hives"].get(hive_id)
    if hive is None or not hive.get("queen"):
        return False
    if not isinstance(amount, (int, float)) or amount <= 0:
        return False
    state["honey"] = min(MAX_HONEY, state["honey"] + amount)
    return True


def honey_by_weight(state):
    return state["honey"]


def cancel_harvest(state, hive_id, amount):
    if not isinstance(amount, (int, float)) or amount <= 0:
        return False
    state["honey"] = max(0, state["honey"] - amount)
    return True


def count_honey(state, hive_id):
    hive = state["hives"].get(hive_id)
    if hive is None or not hive.get("queen"):
        return False
    return True


def disease(state):
    season = state.get("season")
    if state.get("last_disease_season") == season:
        return False
    for hive in state["hives"].values():
        population = hive.get("population", 0)
        loss = max(1, population // 10) if population > 0 else 0
        hive["population"] = max(0, population - loss)
    state["last_disease_season"] = season
    return True


def work(state):
    if state.get("weather") in BAD_WEATHER:
        return False
    return True


def main():
    state = new_game()
    print("养蜂场 - 命令: register/harvest/weight/cancel/count/disease/work/quit")
    handlers = ("register", "harvest", "weight", "cancel", "count", "disease", "work")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        cmd, args = parts[0], parts[1:]
        if cmd not in handlers:
            print("非法命令")
            continue
        try:
            if cmd == "register":
                ok = len(args) == 1 and register_hive(state, args[0])
                print("ok" if ok else "失败")
            elif cmd == "harvest":
                ok = len(args) == 2 and harvest(state, args[0], int(args[1]))
                print("ok" if ok else "失败")
            elif cmd == "weight":
                print(honey_by_weight(state))
            elif cmd == "cancel":
                ok = len(args) == 2 and cancel_harvest(state, args[0], int(args[1]))
                print("ok" if ok else "失败")
            elif cmd == "count":
                ok = len(args) == 1 and count_honey(state, args[0])
                print("ok" if ok else "失败")
            elif cmd == "disease":
                print("ok" if disease(state) else "失败")
            elif cmd == "work":
                print("ok" if work(state) else "失败")
        except (ValueError, TypeError):
            print("参数非法")


if __name__ == "__main__":
    main()
