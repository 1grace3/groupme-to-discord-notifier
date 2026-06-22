import os
import json
import requests

from flask import Flask, request

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

#Do NOT share or push to github your bot_id or discord webhook url, or other people could post unauthorized messages.
#This is set up so that you will enter env variables to your server like Render
BOT_ID =  os.environ["GROUPME_BOT_ID"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

GROUPME_BOT_URL = 'https://api.groupme.com/v3/bots/post' 




#list of admin ids will be set in Render Dashboard so we don't have to edit the code everytime a new mod is added.
ALLOWED_USER_IDS = set()
for uid in os.environ.get("ALLOWED_USER_IDS", "").split(","):
    uid = uid.strip()
    if uid:
        ALLOWED_USER_IDS.add(uid)


MAX_MESSAGE_LENGTH = 2000


def send_discord_announcement(msg, file_urls=None):
    embeds = []
    if file_urls:
        for url in file_urls:
            embeds.append({
                "image" : {"url" : url}
            })

    data = {
        'content' : msg,
        'embeds' : embeds
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data, timeout=10)
        print("\n DISCORD RESPONSE !")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return response.status_code
    
    except Exception as e:
        print("ERROR SENDING DISCORD MESSAGE:", e)
        return None


def send_message(msg):
    data = {
            'bot_id' : BOT_ID, 
            'text' : msg,
    }
    try:
        response = requests.post(GROUPME_BOT_URL, json=data, timeout=10)
        print("\n GROUPME RESPONSE !")
        print("Status:", response.status_code)
        print("Body:", response.text)
        return response.status_code
    
    except Exception as e:
        print("ERROR SENDING MESSAGE:", e)
        return None



@app.route("/")
def home():
   return "Bot is running"

@app.route(f"/groupme/", methods=['POST'])
def hook():
    if not request.is_json:
        return "", 400

    data = request.get_json()
    sender = data.get("name")
    user_id = data.get("user_id")
    sender_type = data.get("sender_type")
    text = data.get("text")

    if not data:
        return "Invalid payload", 400
    
    if sender_type == "bot":
        return "", 200
    
    if text is None:
        return "Missing text", 400
    
    if len(text) > MAX_MESSAGE_LENGTH:
        send_message("Message is too long and could not be sent. (MAX 2000 chars)")
        return "", 400


    if not text.startswith("!announce"):
       #print("Ignoring non-command message")
       return "", 200
    
    print(f"\n Announcement Request from {sender} user id: {user_id}")

    if user_id not in ALLOWED_USER_IDS:
        send_message("You are not authorized to send announcements.")
        return "ok", 200

    announcement = text[len("!announce"):].strip()

    if not announcement:
        send_message("Usage: !announce <message>")
        return "ok", 200
    
    attachments = data.get("attachments", [])
    file_urls = []
    for a in attachments:
        if a.get("type") in ("image", "video", "audio"):
            file_urls.append(a.get("url"))
            
    try:
        send_discord_announcement(f"{announcement}", file_urls)
        send_message("Announcement sent to Discord!")
    except Exception as e:
        print(f"Error: {e}")
        return "", 200

    return "ok", 200



if __name__ == '__main__':
    app.run(debug=False)
