import os
import sys
import ctypes
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
        setup_command = f'netsh wlan set hostednetwork mode=allow ssid="{ssid}(mdp: {password})" key="{password}"'
        start_command = 'netsh wlan start hostednetwork'

        os.system(setup_command)
        os.system(start_command)

        print(f"\nThe WiFi is deployed, its SSID is: {ssid} (mdp: {password})")
        print(f"The password is: {password}")

        # Start viewer.py in the background with a new cmd window
        subprocess.Popen(['start', 'cmd', '/k', f'python viewer.py'], shell=True)

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
        stop_command = 'netsh wlan stop hostednetwork'
        os.system(stop_command)

        time.sleep(2)

        remove_profile_command = 'netsh wlan delete profile name="NeuilleWifi2"'
        os.system(remove_profile_command)

        print("Hotspot stopped and removed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
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
