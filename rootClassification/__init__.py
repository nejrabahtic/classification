from flask import Flask

app = Flask(__name__)

with open('messages.txt', 'r') as f:
    messages = f.readlines()

dictionary = {
    "asyncwait": [
        "async", "await", "wait", "delay", "flaky", "flakiness", "sleep",
        "threads", "synchronization"
    ],
    "concurrency": [
        "concurrency", "flakiness", "flaky", "parallel", "execution",
        "waiting", "mapping", "block"
    ],
    "testorder":
    ["test", "order", "flaky", "flakiness", "dependency", "other"]
}

from rootClassification import routes
