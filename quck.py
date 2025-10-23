#!/usr/bin/env python3

import os
import platform
import subprocess

def detect_distro():
    try:
        with open("/etc/os-release") as f:
            data = f.read().lower()
            if "debian" in data or "ubuntu" in data:
                return "debian"
            elif "arch" in data:
                return "arch"
    except:
        pass
    return "unknown"

def clear_bash_history():
    home = os.path.expanduser("~")
    hist = os.path.join(home, ".bash_history")
    if os.path.exists(hist):
        open(hist, "w").close()
        print("[+] Bash history cleared.")
    else:
        print("[-] No bash history found.")

def clear_var_log():
    log_path = "/var/log"
    if os.geteuid() != 0:
        print("[-] Root permission is required to clean /var/log")
        return

    for root, dirs, files in os.walk(log_path):
        for file in files:
            path = os.path.join(root, file)
            try:
                open(path, "w").close()
                print(f"[+] cleared: {path}")
            except:
                print(f"[!] skipped: {path}")

def clear_leftovers(distro):
    home = os.path.expanduser("~")
    targets = [
        os.path.join(home, ".cache"),
        os.path.join(home, ".local/share/recently-used.xbel")
    ]
    for path in targets:
        if os.path.exists(path):
            if os.path.isfile(path):
                open(path, "w").close()
                print(f"[+] deleted: {path}")
            elif os.path.isdir(path):
                subprocess.call(["rm", "-rf", path])
                print(f"[+] folder deleted: {path}")

    if distro == "debian":
        subprocess.call(["sudo", "truncate", "-s", "0", "/var/log/apt/history.log"])
    elif distro == "arch":
        subprocess.call(["sudo", "truncate", "-s", "0", "/var/log/pacman.log"])
        subprocess.call(["sudo", "journalctl", "--vacuum-time=1s"])

    print("[+] The remains were cleared.")

def main_menu():
    distro = detect_distro()
    print(f"\n Distribution detected: {distro.upper()}\n")

    while True:
        print("""
[1] Clear bash history
[2] Clear the contents of /var/log
[3] Erase residue and traces
[0] Quit
""")
        choice = input("choice > ").strip()

        if choice == "1":
            clear_bash_history()
        elif choice == "2":
            clear_var_log()
        elif choice == "3":
            clear_leftovers(distro)
        elif choice == "0":
            break
        else:
            print("Enter a valid option.")

if __name__ == "__main__":
    main_menu()
