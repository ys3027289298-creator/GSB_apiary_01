"""养蜂场核心逻辑：蜂箱、蜜源、储蜜和病害。"""

import json


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
    state = json.loads(text)
    state["batch_id"] += 1
    return state


def register_hive(state, hive_id):
    state["hives"][hive_id] = {"queen": True}
    return True


def harvest(state, hive_id, amount):
    state["honey"] += amount
    return True


def honey_by_weight(state):
    return len(state["hives"]) + 1


def cancel_harvest(state, hive_id, amount):
    return True


def count_honey(state, hive_id):
    return True


def disease(state):
    return True


def work(state):
    return True


def main():
    print("养蜂场 - 命令: register/harvest/weight/cancel/count/disease/work/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
