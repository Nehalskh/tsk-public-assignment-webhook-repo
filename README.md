# GitHub Webhook Receiver + MongoDB Viewer (Flask)

This project receives GitHub webhook events (Push, Pull Request, Merge), stores them in MongoDB, and displays the latest events in a simple HTML UI that auto-refreshes every 15 seconds.

---

## ✅ Features

- Receives GitHub webhook events:
  - **PUSH**
  - **PULL_REQUEST**
  - **MERGE** (bonus / brownie points)
- Stores events in **MongoDB** with schema:
  - request_id
  - author
  - action
  - from_branch
  - to_branch
  - timestamp
- UI refreshes every **15 seconds** and shows formatted event messages.

---

## 🛠️ Tech Stack

- Python (Flask)
- MongoDB (Local)
- HTML + JavaScript (Polling UI)
- ngrok (Expose localhost to GitHub webhook)

---

## 📁 Project Structure

