# utils.py
import json

def save_params(filename, params):
    with open(filename, "w") as f:
        json.dump(params, f, indent=2)
    print(f"參數已儲存至 {filename}")

def load_params(filename):
    with open(filename, "r") as f:
        params = json.load(f)
    print(f"參數已載入 {filename}")
    return params
