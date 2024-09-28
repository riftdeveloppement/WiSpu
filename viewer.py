import os
import subprocess
import time
import re

def sanitize_device_name(device_name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', device_name)

def create_dist_directory():
    if not os.path.exists("dist"):
        os.makedirs("dist")

def get_connected_devices():
    try:
        result = subprocess.check_output(['arp', '-a'], stderr=subprocess.STDOUT, text=True)
        return result.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving connected devices: {e.output}")
        return []

def extract_device_info(line):
    parts = line.split()
    if len(parts) > 1:
        ip_address = parts[1].strip('()')
        device_name = parts[0]
        return device_name, ip_address
    return None, None

def get_mac_vendor(mac_address):
    # Example logic to get the MAC vendor, which can help identify the device
    # This function can call an API or look up a database
    # For this example, we will return a dummy value
    return "DummyVendor"  # Replace with actual vendor lookup

def collect_additional_info(ip_address):
    # Here you can include logic to collect more information if available
    # This is a dummy example for demonstration purposes
    email = "example@example.com"  # Placeholder, replace with actual logic to retrieve email
    first_name = "John"  # Placeholder
    last_name = "Doe"  # Placeholder
    phone_number = "123-456-7890"  # Placeholder
    return email, first_name, last_name, phone_number

def create_device_file(device_name, device_info):
    sanitized_name = sanitize_device_name(device_name)
    file_path = os.path.join("dist", f"{sanitized_name}.txt")
    
    if os.path.exists(file_path):
        print(f"File for {device_name} already exists. Skipping...")
        return
    
    email, first_name, last_name, phone_number = collect_additional_info(device_info)
    
    with open(file_path, 'w') as file:
        file.write(f"Device Name: {device_name}\n")
        file.write(f"IP Address: {device_info}\n")
        file.write(f"MAC Address: {get_mac_vendor(device_info)}\n")  # Dummy example, needs real MAC address
        file.write(f"Email: {email}\n")
        file.write(f"First Name: {first_name}\n")
        file.write(f"Last Name: {last_name}\n")
        file.write(f"Phone Number: {phone_number}\n")
    
    print(f"Created file for {device_name} with IP {device_info}")

def monitor_new_devices():
    seen_devices = set()  # Set to keep track of seen devices
    create_dist_directory()  # Ensure the 'dist' directory exists
    print("viewer.py is running, monitoring new devices...")
    
    while True:
        devices = get_connected_devices()
        current_devices = set()  # Track devices in this iteration
        
        for device in devices:
            device_name, ip_address = extract_device_info(device)
            if device_name and ip_address:
                current_devices.add(device_name)  # Add to current devices
                if device_name not in seen_devices:
                    create_device_file(device_name, ip_address)
                    seen_devices.add(device_name)  # Mark as seen for future iterations
        
        # Remove devices not seen this iteration from the seen_devices set
        seen_devices.intersection_update(current_devices)
        
        time.sleep(5)  # Adjust the sleep time as needed

if __name__ == "__main__":
    monitor_new_devices()
