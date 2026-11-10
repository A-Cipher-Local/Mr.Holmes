import urllib.request
import json

# Replace with your actual Discord or Telegram Bot Webhook URL (or leave blank to disable)
WEBHOOK_URL = ""

def send_entity_alert(record_title, matched_entities, video_id):
    """Pushes real-time multi-entity alerts to a webhook using built-in urllib."""
    if not WEBHOOK_URL or "YOUR_WEBHOOK" in WEBHOOK_URL:
        return

    payload = {
        "content": f"[!] **PROJECT ARGUS ALERT**\n"
                   f"**Multi-Entity Co-Occurrence Detected!**\n"
                   f"- **Title:** {record_title}\n"
                   f"- **Entities:** {', '.join(matched_entities)}\n"
                   f"- **Target ID:** {video_id}"
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "ArgusDaemon/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status not in [200, 204]:
                print(f"[-] Webhook alert returned status {response.status}")
    except Exception as e:
        print(f"[-] Webhook transmission error: {str(e)}")

import urllib.request
import json

WEBHOOK_URL = ""

def send_entity_alert(record_title, matched_entities, video_id):
    if not WEBHOOK_URL or "YOUR_WEBHOOK" in WEBHOOK_URL:
        return
    payload = {
        "content": f"[!] **PROJECT ARGUS ALERT**\n"
                   f"**Multi-Entity Co-Occurrence Detected!**\n"
                   f"- **Title:** {record_title}\n"
                   f"- **Entities:** {', '.join(matched_entities)}\n"
                   f"- **Target ID:** {video_id}"
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json", "User-Agent": "ArgusDaemon/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status not in [200, 204]:
                print(f"[-] Webhook alert returned status {response.status}")
    except Exception as e:
        print(f"[-] Webhook transmission error: {str(e)}")
