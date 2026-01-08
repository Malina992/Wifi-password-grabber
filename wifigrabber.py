import subprocess
import os
import re

def get_unique_filename(base_name="wynik", extension=".txt"):
    filename = f"{base_name}{extension}"
    if not os.path.exists(filename):
        return filename
    
    counter = 1
    while True:
        filename = f"{base_name}{counter:03d}{extension}"
        if not os.path.exists(filename):
            return filename
        counter += 1

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True).decode('cp852', errors='ignore')
        return result
    except subprocess.CalledProcessError:
        return ""

def main():
    output_file = get_unique_filename()
    print(f"Saving to file: {output_file}")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("--- netsh results ---\n")
        
        
        raw_profiles = run_command("netsh wlan show profiles")
        
        profiles = re.findall(r":\s*(.*)", raw_profiles)
        
        valid_profiles = []
        for line in raw_profiles.split('\n'):
            if "All User Profile" in line or "Wszystkie profile" in line:
                parts = line.split(":")
                if len(parts) > 1:
                    valid_profiles.append(parts[1].strip())

        for profile in valid_profiles:
            print(f"Processing: {profile}")
            f.write(f"\n===== Profile: {profile} =====\n")
            
            details = run_command(f'netsh wlan show profile name="{profile}" key=clear')
            f.write(details)

    print(f"\nPasswords saved in: {output_file}")

if __name__ == "__main__":
    main()
