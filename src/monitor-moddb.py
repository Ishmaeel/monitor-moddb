from bs4 import BeautifulSoup
import json
import os
import os.path
import requests
import sys
import uuid

ADDON_NAME = sys.argv[1] if len(sys.argv) > 1 else None

if not ADDON_NAME:
    exit("Cannot check for comments without addon name.")

STASH_ROOT = "moddb-stash"
if not os.path.isdir(STASH_ROOT):
    os.mkdir(STASH_ROOT)

PROJECT_ID = int(os.environ["PROJECT_ID"]
                 ) if "PROJECT_ID" in os.environ else None

API_KEY = os.environ["TODOIST_API_KEY"] if "TODOIST_API_KEY" in os.environ else None

EXCLUDE_AUTHOR = os.environ["EXCLUDE_AUTHOR"] if "EXCLUDE_AUTHOR" in os.environ else None

addon_url = f"https://www.moddb.com/addons/{ADDON_NAME}/page/9999"
stash = f"{STASH_ROOT}/{ADDON_NAME}.txt"
stash_old = f"{STASH_ROOT}/{ADDON_NAME}.old"
subject = f"New comment on {ADDON_NAME}"
contents = [addon_url]

request_headers = {
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

response = requests.get(addon_url, headers=request_headers)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for li in soup.select("div.row a.author"):
    if li.text != EXCLUDE_AUTHOR:
        contents.append(li.text)

current = "\n".join(contents)
print(f"{current}\n")

previous = ""
if os.path.exists(stash):
    with open(stash, encoding="utf-8") as f:
        previous = f.read()

if previous == current:
    print("no change")
else:
    print("change!")

    if not API_KEY:
        exit("Cannot create Todoist item without API KEY. Exiting.")

    if not PROJECT_ID:
        exit("Cannot create Todoist item without PROJECT ID. Exiting.")

    response = requests.get("https://api.todoist.com/rest/v2/tasks",
                            params={
                                "project_id": PROJECT_ID,
                                "filter": f"search:{subject}"
                            },
                            headers={
                                "Authorization": f"Bearer {API_KEY}"
                            })

    print(f"response: {response}")

    existing = response.json()

    print("existing task count: %s" % len(existing))

    if len(existing) == 0:
        print("creating new task...")
        response = requests.post("https://api.todoist.com/rest/v2/tasks",
                                 data=json.dumps({
                                     "content": f"[{subject}]({addon_url})",
                                     "project_id": PROJECT_ID,
                                     "due_string": "today"
                                 }),
                                 headers={
                                     "Content-Type": "application/json",
                                     "X-Request-Id": str(uuid.uuid4()),
                                     "Authorization": f"Bearer {API_KEY}"
                                 })
        response.raise_for_status()

    with open(stash_old, "w", encoding="utf-8") as f:
        f.write(previous)

with open(stash, "w", encoding="utf-8") as f:
    f.write(current)
