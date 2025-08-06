#!/data/data/com.termux/files/usr/bin/python

try:
    import ipapi
except ImportError:
    print("❌ ipapi module not found. Please install it using: pip install ipapi")
    exit()

import csv
import os
import time

# Fallback colors
class c:
    ran = '\033[96m'    # Cyan
    c = '\033[93m'      # Yellow
    lr = '\033[91m'     # Red
    lg = '\033[92m'     # Light Green
    boldg = '\033[1;92m'  # Bold Green
    reset = '\033[0m'   # Reset

def banner():
    print(c.lg + "\n╔═[ IP INFO LOCATOR TOOL ]" + c.reset)

def banner2():
    print(c.lg + "╚═[ Session Ended ]" + c.reset)

def clear():
    os.system("clear")

def locat(location):
    if location and 'latitude' in location and 'longitude' in location:
        lat = location["latitude"]
        lon = location["longitude"]
        link = f"https://www.google.com/maps/place/{lat},{lon}"
        print(f"\n🌐 {c.lg}Google Maps Link:{c.reset} {link}")
        return link
    else:
        print("⚠️ Location data unavailable.")
        return "N/A"

def save_to_csv(ip, location, google_maps_link):
    csv_file = 'ip_details.csv'
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(['Attribute', 'Value'])

        writer.writerow(['\n\n'])
        writer.writerow(['IP Address', ip])

        keys = [
            'network', 'version', 'city', 'region', 'region_code', 'country',
            'country_name', 'country_code', 'country_code_iso3', 'country_capital',
            'country_tld', 'continent_code', 'in_eu', 'postal', 'latitude',
            'longitude', 'timezone', 'utc_offset', 'country_calling_code',
            'currency', 'currency_name', 'languages', 'country_area',
            'country_population', 'asn', 'org'
        ]

        for key in keys:
            writer.writerow([key.replace('_', ' ').title(), location.get(key, '')])

        writer.writerow(['Google Maps Link', google_maps_link])

def program():
    try:
        ip = input(c.ran + "🔍 Enter target IP: " + c.reset).strip()
        if ip == "":
            print(c.lr + "❌ IP cannot be empty." + c.reset)
            return
        location = ipapi.location(ip)

        print("\n📍 IP Details:\n")
        for k, v in location.items():
            label = k.replace("_", " ").title()
            if label.lower() in ["weight", "result"]:
                print(f"{c.boldg}✅ ➤ {label:<25}: {v}{c.reset}")
            else:
                print(f"{c.lg}➤ {label:<25}: {v}{c.reset}")

        google_maps_link = locat(location)
        save_to_csv(ip, location, google_maps_link)

    except KeyboardInterrupt:
        print(c.lr + "\n⛔ Interrupted by user (Ctrl+C). Returning to menu...\n" + c.reset)
    except Exception as e:
        print(c.lr + f"[Error] {str(e)}" + c.reset)

# ──────────────── Main Loop ────────────────

yes = ['y', 'yes']
no = ['n', 'no']

while True:
    try:
        clear()
        banner()
        program()
        cont = input(c.lg + "\n🔁 Do you want to continue? [y/n] " + c.reset).strip().lower()
        if cont in no:
            clear()
            banner2()
            print(c.lr + "\n🚪 Exiting the tool. Goodbye!\n" + c.reset)
            break
    except KeyboardInterrupt:
        print(c.lr + "\n🚪 Exit requested by user. Goodbye!\n" + c.reset)
        break
                    
