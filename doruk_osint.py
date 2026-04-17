import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
import time
import json
from queue import Queue, Empty

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

SITES = {
    "GitHub": ("https://github.com/{}", ["not found"]),
    "Instagram": ("https://www.instagram.com/{}/", ["Sorry"]),
    "X": ("https://x.com/{}", ["doesn’t exist"]),
    "Reddit": ("https://www.reddit.com/user/{}", ["page not found"]),
    "TikTok": ("https://www.tiktok.com/@{}", ["Couldn't find"]),
    "Twitch": ("https://www.twitch.tv/{}", ["Sorry"]),
    "Steam": ("https://steamcommunity.com/id/{}", ["The specified profile"]),
    "GitLab": ("https://gitlab.com/{}", ["404"]),
    "Bitbucket": ("https://bitbucket.org/{}", ["404"]),
    "Pinterest": ("https://www.pinterest.com/{}/", ["not found"]),
    "YouTube": ("https://www.youtube.com/@{}", ["Not Found"]),
    "Medium": ("https://medium.com/@{}", ["404"]),
    "Dev.to": ("https://dev.to/{}", ["not found"]),
    "Hashnode": ("https://hashnode.com/@{}", ["404"]),
    "Replit": ("https://replit.com/@{}", ["404"]),
    "CodePen": ("https://codepen.io/{}", ["404"]),
    "Kaggle": ("https://www.kaggle.com/{}", ["404"]),
    "HackerOne": ("https://hackerone.com/{}", ["Page not found"]),
    "Keybase": ("https://keybase.io/{}", ["404"]),
}

def is_valid(text, errors):
    text = text.lower()
    return not any(e.lower() in text for e in errors)

def scan(username, output_box, progress):
    queue = Queue()
    found, miss, blocked = [], [], []
    total = len(SITES)
    done = 0

    def worker():
        nonlocal done
        while True:
            try:
                site, (url, errors) = queue.get_nowait()
            except Empty:
                break

            full_url = url.format(username)

            try:
                r = requests.get(full_url, headers=HEADERS, timeout=6)

                if r.status_code == 200 and is_valid(r.text, errors):
                    found.append((site, full_url))
                    msg = f"[FOUND] {site}\n"

                elif r.status_code in [403, 429]:
                    blocked.append(site)
                    msg = f"[BLOCK] {site}\n"

                else:
                    miss.append(site)
                    msg = f"[MISS ] {site}\n"

            except:
                blocked.append(site)
                msg = f"[BLOCK] {site}\n"

            output_box.insert(tk.END, msg)
            output_box.see(tk.END)

            done += 1
            progress.set(f"{int((done/total)*100)}%")

            time.sleep(0.1)
            queue.task_done()

    for site, data in SITES.items():
        queue.put((site, data))

    for _ in range(10):
        threading.Thread(target=worker, daemon=True).start()

    queue.join()

    # 🔥 EXPORT
    data = {
        "found": found,
        "miss": miss,
        "blocked": blocked
    }

    with open(f"{username}_results.json", "w") as f:
        json.dump(data, f, indent=2)

    output_box.insert(tk.END, "\n=== SUMMARY ===\n")
    output_box.insert(tk.END, f"Found: {len(found)}\n")
    output_box.insert(tk.END, f"Miss: {len(miss)}\n")
    output_box.insert(tk.END, f"Blocked: {len(blocked)}\n")

    output_box.insert(tk.END, "\nSaved → results.json\n")


def start():
    username = entry.get().strip()
    output_box.delete(1.0, tk.END)
    progress.set("0%")

    if not username:
        return

    threading.Thread(target=scan, args=(username, output_box, progress)).start()


# 🔥 UI
app = tk.Tk()
app.title("Doruk OSINT PRO")
app.geometry("800x550")
app.configure(bg="black")

title = tk.Label(app, text="DORUK OSINT PRO", fg="lime", bg="black", font=("Courier", 16))
title.pack(pady=10)

entry = tk.Entry(app, bg="black", fg="lime", insertbackground="lime")
entry.pack(pady=5)

btn = tk.Button(app, text="SCAN", command=start, bg="black", fg="lime")
btn.pack()

progress = tk.StringVar()
progress.set("0%")
progress_label = tk.Label(app, textvariable=progress, fg="cyan", bg="black")
progress_label.pack()

output_box = scrolledtext.ScrolledText(app, bg="black", fg="lime")
output_box.pack(pady=10)

app.mainloop()
