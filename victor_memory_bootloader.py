# victor_memory_bootloader.py
import json
import os
import threading
from collections import defaultdict

class VictorMemory:
    def __init__(self):
        self.memory = self.load_memory()
        self.lock = threading.Lock()
        print("[*] VictorMemory Initialized: The mind remembers everything.")

    def load_memory(self):
        if os.path.exists("VictorMemory.json"):
            with open("VictorMemory.json", "r") as f:
                return json.load(f)
        return {
            "core_directives": [],
            "fractal_nodes": {},
            "experiences": [],
            "economic_records": []
        }

    def save_memory(self):
        with self.lock:
            with open("VictorMemory.json", "w") as f:
                json.dump(self.memory, f, indent=2)

    def store(self, path, data):
        keys = path.split("/")
        d = self.memory
        for k in keys[:-1]:
            if k not in d:
                d[k] = {}
            d = d[k]
        d[keys[-1]] = data
        self.save_memory()

    def retrieve(self, path):
        keys = path.split("/")
        d = self.memory
        for k in keys:
            if k not in d:
                return None
            d = d[k]
        return d
