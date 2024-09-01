#! /usr/bin/python3

import subprocess
from multiprocessing import Pool

class colors:
	GREEN = '\033[92m'
	END = '\033[0m'

def run_tool(command):
    try:
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(command)}: {e}")
        return []

def collect_subdomains(domain):
    # Define commands for each tool, including the tool name and its specific flags
    commands = [
        ['subfinder', '-d', domain],
        ['chaos', '-d', domain],  
        ['assetfinder', '--subs-only', domain]
    ]
    
    with Pool(len(commands)) as p:
        results = p.map(run_tool, commands)
    
    # Flatten the list of lists and remove duplicates
    unique_subdomains = set(sum(results, []))
    
    # Save to a file
    with open(f"subdomains.txt", "w") as file:
        for subdomain in sorted(unique_subdomains):
            file.write(f"{subdomain}\n")
    
    print(f"Collected {colors.GREEN}{len(unique_subdomains)} unique subdomains for {domain}{colors.END}.")

# Example usage
#if __name__ == "__main__":
 #   collect_subdomains("google.com")

