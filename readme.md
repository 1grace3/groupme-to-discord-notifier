# GroupMe -> Discord Notifier

When an authorized user sends `!announce <message>` in your GroupMe, it forwards the message to a Discord channel via webhook. Supports images, GIFs, and video attachments.

---

## Setup

### 1. Create a GroupMe bot
Go to https://dev.groupme.com/bots and create a bot. Note down your **Bot ID**. Leave the callback URL blank for now.

### 2. Create a Discord webhook
In your Discord server, go to **Server Settings -> Integrations -> Webhooks -> New Webhook**. Select the channel you want announcements posted in and copy the webhook URL.

### 3. Host the app
Deploy the app to a hosting service. Some options:

| Option | Notes |
|--------|-------|
| [Render](https://render.com/) | Recommended. has a free plan |
| [Heroku](https://heroku.com/) | Popular alternative |
| [Fly.io](https://fly.io/) | Another solid option |
| Self-hosted | An old laptop or Raspberry Pi works fine |

> **For local testing:** Use [ngrok](https://ngrok.com/) to expose your localhost as a public URL.

### 4. Deploy the web service
Clone this repo (or paste its URL) into your hosting service. On Render, create a new **Project -> Web Service**, connect your repo, or click below:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/1grace3/groupme-to-discord-notifier)

Add the following:

**Start command:**
```
gunicorn app:app
```

**Build Command**
```bash
pip install -r requirements.txt
```

**Environment variables:**

| Name | Description | Example |
|------|-------------|---------|
| `ALLOWED_USER_IDS` | GroupMe user IDs allowed to use `!announce` | `129743,124509` |
| `DISCORD_WEBHOOK_URL` | Your Discord webhook URL | `https://discord.com/api/webhooks/123...` |
| `GROUPME_BOT_ID` | Your GroupMe bot ID | `abcd12345fe` |
| `WEBHOOK_SECRET` | A random string you make up, or under "add variable" in render, add "generated secret" | `U138BFjiwuhkb249` |

---

#### Finding your allowed user IDs

Only users listed in `ALLOWED_USER_IDS` can trigger `!announce`. To find them, you'll need your **access token** (find it at [dev.groupme.com](https://dev.groupme.com) under your profile picture) and your **group ID**.

**Option A: browser:** Paste this URL and inspect the JSON under `members`:
```
https://api.groupme.com/v3/groups/YOUR_GROUP_ID?token=YOUR_ACCESS_TOKEN
```

**Option B: script:** Run the included helper script, which prints each admin's name and a ready-to-paste list of IDs:
```bash
python get_groupme_admins.py YOUR_ACCESS_TOKEN YOUR_GROUP_ID
```

Paste the output IDs as a plain, comma-separated list.
> (The script only returns group admins. To allow a non-admin user, use Option A to look up their `user_id` manually and add it to the list.)

---

### 5. Deploy and verify
Click **Deploy Web Service**. Once it finishes, open the provided `.onrender.com` URL. If you see a white page that says **"Bot is running"**, it's working.

### 6. Set the GroupMe callback URL
Take that URL and append `/groupme/<your_webhook_secret>/`:

```
ex) https://your-app-name.onrender.com/groupme/U138BFjiwuhkb249/
```

Go back to https://dev.groupme.com/bots, edit your bot, and paste this as the **Callback URL**.

### 7. Test it
Send `!announce Hello world` in your GroupMe. The message should appear in your Discord channel.
