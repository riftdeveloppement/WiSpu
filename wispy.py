import os
import sys
import subprocess
import time

def print_title():
    title = """
                                     ██╗    ██╗██╗███████╗██████╗ ██╗   ██╗
                                     ██║    ██║██║██╔════╝██╔══██╗╚██╗ ██╔╝
                                     ██║ █╗ ██║██║███████╗██████╔╝ ╚████╔╝ 
                                     ██║███╗██║██║╚════██║██╔═══╝   ╚██╔╝   
                                     ╚███╔███╔╝██║███████║██║        ██║   
                                      ╚══╝╚══╝ ╚═╝╚══════╝╚═╝        ╚═╝                       
    """
    print(title)

def print_menu():
    menu = """
                                +--------------------------+   +--------------+ 
                                | 1: Deploy the WiFi       |   | 2: Exit      |
                                +--------------------------+   +--------------+
    """
    print(menu)

def create_and_start_hotspot(ssid, password):
    try:
        # Create and start the WiFi hotspot using nmcli (NetworkManager Command Line Interface)
        setup_command = f'nmcli dev wifi hotspot ifname wlan0 ssid "{ssid}" password "{password}"'
        os.system(setup_command)

        print(f"\nThe WiFi is deployed, its SSID is: {ssid} (mdp: {password})")
        print(f"The password is: {password}")

        # Start viewer.py in the background with a new terminal window
        subprocess.Popen(['gnome-terminal', '--', 'python3', 'viewer.py'])

        print("\n1: Stop the hotspot")

        while True:
            choice = input("Choose an option: ")

            if choice == '1':
                stop_hotspot()
                break
            elif choice != '1':
                continue

    except Exception as e:
        print(f"An error occurred: {e}")

def stop_hotspot():
    try:
        # Stop the hotspot using nmcli
        stop_command = 'nmcli connection down Hotspot'
        os.system(stop_command)
        
        print("Hotspot stopped successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_admin():
    try:
        return os.geteuid() == 0  # Checks if the script is running as root (admin)
    except:
        return False

def run_as_admin():
    if not is_admin():
        print("This script needs to be run as root. Please restart it with sudo.")
        sys.exit()

def main():
    run_as_admin()

    while True:
        print_title()
        print_menu()

        choice = input("Choose an option: ")

        if choice == '1':
            ssid = "EDGAR"
            password = "edgar64230"
            create_and_start_hotspot(ssid, password)
        elif choice == '2':
            sys.exit()
        else:
            print("Invalid choice. Please try again.")
            continue

if __name__ == "__main__":
    main()
