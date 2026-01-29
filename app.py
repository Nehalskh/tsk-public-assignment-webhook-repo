from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timezone
import os

app = Flask(__name__)

# Local MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["github_webhooks"]
events = db["events"]  # collection

def utc_string():
    return datetime.now(timezone.utc).strftime("%d %B %Y - %I:%M %p UTC")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event", "")
    payload = request.get_json(silent=True) or {}

    doc = None

    # PUSH event
    if event_type == "push":
        author = payload.get("pusher", {}).get("name") or payload.get("sender", {}).get("login") or "Unknown"
        to_branch = (payload.get("ref") or "").split("/")[-1]
        request_id = payload.get("after")  # commit hash

        doc = {
            "request_id": str(request_id),
            "author": str(author),
            "action": "PUSH",
            "from_branch": None,
            "to_branch": str(to_branch),
            "timestamp": utc_string()
        }

    # PULL REQUEST + MERGE events
    elif event_type == "pull_request":
        pr_action = payload.get("action")  # opened, reopened, closed, etc.
        pr = payload.get("pull_request", {})

        author = pr.get("user", {}).get("login") or "Unknown"
        from_branch = pr.get("head", {}).get("ref")
        to_branch = pr.get("base", {}).get("ref")
        request_id = pr.get("id")  # PR id
        merged = bool(pr.get("merged", False))

        # MERGE: closed + merged true
        if pr_action == "closed" and merged:
            doc = {
                "request_id": str(request_id),
                "author": str(author),
                "action": "MERGE",
                "from_branch": str(from_branch),
                "to_branch": str(to_branch),
                "timestamp": utc_string()
            }

        # PR opened/reopened
        elif pr_action in ("opened", "reopened"):
            doc = {
                "request_id": str(request_id),
                "author": str(author),
                "action": "PULL_REQUEST",
                "from_branch": str(from_branch),
                "to_branch": str(to_branch),
                "timestamp": utc_string()
            }

    # Store only supported events
    if doc:
        events.insert_one(doc)
        return jsonify({"status": "stored"}), 200

    return jsonify({"status": "ignored"}), 200


#  API for UI polling
@app.route("/events", methods=["GET"])
def get_events():
    latest = list(events.find({}, {"_id": 0}).sort([("_id", -1)]).limit(20))
    return jsonify(latest), 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
