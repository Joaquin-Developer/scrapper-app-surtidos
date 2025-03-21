import sys
import os
import json
from typing import List, Dict, Any


DEFAULT_JSON_DIR = "data/raw/"


def load_json(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def print_values(paths: List[str]):
    for path in paths:
        print(f"File: {path}")
        json_data = load_json(path)
        total = 0
        for elem in json_data:
            url = elem["url"]
            data = elem["data"]
            data_len = len(data)
            total += data_len
            print(f"{url} : {data_len}")
        print(f"Total: {total}\n")


def main(json_path: str):
    if ".json" in json_path:
        return print_values([json_path])
    paths = [f"{DEFAULT_JSON_DIR}{f}" for f in os.listdir(DEFAULT_JSON_DIR) if f.endswith(".json")]
    print_values(paths)


if __name__ == "__main__":
    main(sys.argv[-1])
