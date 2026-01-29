GitHub Webhook Receiver + MongoDB Viewer (Flask)

This project receives GitHub webhook events (Push, Pull Request, Merge), stores them in MongoDB, and displays the latest events in a simple HTML UI that auto-refreshes every 15 seconds.


1) Features

- Receives GitHub webhook events:
  - PUSH
  - PULL_REQUEST
  - MERGE (bonus/brownie points)
- Stores events in MongoDB with schema:
  - request_id
  - author
  - action
  - from_branch
  - to_branch
  - timestamp
- UI refreshes every 15 seconds and shows formatted event messages.


2) Tech Stack

- Python (Flask)
- MongoDB (Local)
- HTML + JavaScript (Polling UI)
- ngrok (Expose localhost to GitHub webhook)


3) Project Structure

webhook-repo/
  app.py
  requirements.txt
  templates/
    index.html


4) Setup Instructions

Step 1: Start MongoDB locally
Make sure MongoDB service is running (Windows Services).

MongoDB runs on:
mongodb://localhost:27017


Step 2: Install Python dependencies
pip install -r requirements.txt


Step 3: Run the Flask server
python app.py

Server will run at:
http://localhost:5000


Step 4: Start ngrok (for GitHub webhook delivery)
In another terminal:
ngrok http 5000

You will get a public forwarding link like:
https://xxxx.ngrok-free.dev


Step 5: Configure GitHub Webhook (in action-repo)
On your GitHub repo (action-repo):
Settings -> Webhooks -> Add webhook

Payload URL:
https://xxxx.ngrok-free.dev/webhook

Content type:
application/json

Events:
- Pushes
- Pull requests


5) UI Output Format

Push:
{author} pushed to "{to_branch}" on {timestamp}

Pull Request:
{author} submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp}

Merge:
{author} merged branch "{from_branch}" to "{to_branch}" on {timestamp}


6) Testing

Trigger events in your action-repo:

1. Push commits -> should show PUSH in UI
2. Create PR -> should show PULL_REQUEST in UI
3. Merge PR -> should show MERGE in UI

Open UI:
http://localhost:5000


7) Notes

- GitHub cannot call localhost directly, so ngrok is required.
- MongoDB stores events inside:
  Database: github_webhooks
  Collection: events
