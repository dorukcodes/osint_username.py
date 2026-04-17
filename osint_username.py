#!/usr/bin/env python3
# osint_username.py — dorukcodes

import requests
import threading
import argparse
import json
import time
from queue import Queue, Empty
from datetime import datetime

# 🎨 RENKLER
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

# 🔥 BANNER (imza)
BANNER = f"""
{MAGENTA}
╔══════════════════════════════════════╗
║        USERNAME OSINT TOOL           ║
║         github.com/dorukcodes        ║
╚══════════════════════════════════════╝
{RESET}
"""

HEADERS = {"User-Agent": "Mozilla/5.0"}

# 🌐 SİTELER
SITES = {
    "GitHub": ("https://github.com/{}", ["not found"]),
    "Instagram": ("https://www.instagram.com/{}/", ["Sorry, this page isn't available"]),
    "X": ("https://x.com/{}", ["This account doesn’t exist"]),
    "Reddit": ("https://www.reddit.com/user/{}", ["page not found"]),
    "TikTok": ("https://www.tiktok.com/@{}", ["Couldn't find this account"]),
    "Pinterest": ("https://www.pinterest.com/{}/", ["not found"]),
    "YouTube": ("https://www.youtube.com/@{}", ["Not Found"]),
    "Medium": ("https://medium.com/@{}", ["404"]),
    "Twitch": ("https://www.twitch.tv/{}", ["Sorry. Unless you’ve got a time machine"]),
    "GitLab": ("https://gitlab.com/{}", ["404"]),
    "Bitbucket": ("https://bitbucket.org/{}", ["404"]),
    "HackerOne": ("https://hackerone.com/{}", ["Page not found"]),
    "Pastebin": ("https://pastebin.com/u/{}", ["Not Found"]),
    "Kaggle": ("https://www.kaggle.com/{}", ["404"]),
    "Replit": ("https://replit.com/@{}", ["404"]),
    "CodePen": ("https://codepen.io/{}", ["404"]),
    "Dev.to": ("https://dev.to/{}", ["not found"]),
    "Hashnode": ("https://hashnode.com/@{}", ["404"]),
    "ProductHunt": ("https://www.producthunt.com/@{}", ["404"]),
    "Keybase": ("https://keybase.io/{}", ["404"]),
    "Steam": ("https://steamcommunity.com/id/{}", ["404"]),
    "SoundCloud": ("https://soundcloud.com/{}", ["404"]),
    "About.me": ("https://about.me/{}", ["404"]),
}

queue = Queue()
results = []
lock = threading.Lock()

stats = {"found": 0, "not_found": 0, "errors": 0}


def is_valid(text, errors):
    text = text.lower()
    return not any(err.lower() in text for err in errors)


def request_retry(url):
    for _ in range(2):
        try:
            return requests.get(url, headers=HEADERS, timeout=6)
        except:
            time.sleep(0.5)
    return None


def worker(username):
    while True:
        try:
            site, (url, errors) = queue.get_nowait()
        except Empty:
            break

        full_url = url.format(username)
        r = request_retry(full_url)

        if r and r.status_code == 200 and is_valid(r.text, errors):
            with lock:
                print(f"{GREEN}[FOUND] {site:<15}{RESET}")
                results.append((site, full_url))
                stats["found"] += 1
        elif r:
            with lock:
                print(f"{RED}[MISS ] {site:<15}{RESET}")
                stats["not_found"] += 1
        else:
            with lock:
                print(f"{YELLOW}[ERROR] {site:<15}{RESET}")
                stats["errors"] += 1

        time.sleep(0.1)
        queue.task_done()


def save(username, fmt):
    name = f"results_{username}_{datetime.now().strftime('%H%M%S')}"

    if fmt == "txt":
        with open(name + ".txt", "w") as f:
            for s, u in results:
                f.write(f"{s} → {u}\n")

    if fmt == "json":
        with open(name + ".json", "w") as f:
            json.dump(results, f, indent=2)

    print(f"{CYAN}[✔] Results saved → {name}.{fmt}{RESET}")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("--save", choices=["txt", "json"])
    args = parser.parse_args()

    print(f"{CYAN}[+] Target locked → {args.username}{RESET}")
    print(f"{CYAN}[+] Starting scan...{RESET}\n")

    for site, data in SITES.items():
        queue.put((site, data))

    for _ in range(10):
        threading.Thread(target=worker, args=(args.username,), daemon=True).start()

    queue.join()

    print(f"\n{MAGENTA}══════════════════════════════════════{RESET}")
    print(f"{CYAN}[✓] Scan completed{RESET}")
    print(f"{GREEN}Found     : {stats['found']}{RESET}")
    print(f"{RED}Not Found : {stats['not_found']}{RESET}")
    print(f"{YELLOW}Errors    : {stats['errors']}{RESET}")
    print(f"{MAGENTA}══════════════════════════════════════{RESET}")

    if results:
        print(f"\n{CYAN}[+] Discovered Accounts:{RESET}")
        for s, u in results:
            print(f"{GREEN}{s:<15} → {u}{RESET}")
    else:
        print(f"{RED}[!] No accounts found{RESET}")

    print(f"\n{MAGENTA}— dorukcodes OSINT engine finished —{RESET}\n")

    if args.save:
        save(args.username, args.save)


if __name__ == "__main__":
    main()
