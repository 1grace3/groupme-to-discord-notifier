import urllib.request
import json
import argparse

parser = argparse.ArgumentParser(description="Fetch GroupMe admins for a given group.")
parser.add_argument("access_token", help="Your GroupMe access token")
parser.add_argument("group_id", help="The GroupMe group ID")
args = parser.parse_args()

ACCESS_TOKEN = args.access_token
GROUP_ID = args.group_id

url = f"https://api.groupme.com/v3/groups/{GROUP_ID}?token={ACCESS_TOKEN}"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

members = data["response"]["members"]

admins = [m for m in members if "admin" in m.get("roles", []) or "owner" in m.get("roles", [])]

print(f"Found {len(admins)} admin(s):\n")
for m in admins:
    roles = ", ".join(m.get("roles", []))
    print(f"  Name:    {m.get('nickname')}")
    print(f"  User ID: {m.get('user_id')}")
    print(f"  Roles:   {roles}")
    print()

# Optionally dump just the user_ids as a list
admin_ids = [m["user_id"] for m in admins]
print("Admin user_ids:", admin_ids)