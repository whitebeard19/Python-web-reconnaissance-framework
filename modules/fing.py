#! /usr/bin/python3

import subprocess
import json
import re

def parse_whatweb_output(output):
    # Regular expression to match technologies and their versions
    tech_version_regex = re.compile(r'([a-zA-Z0-9\-]+)\[([^\]]+)\]')
    # Dictionary to hold the technology and version
    tech_info = {}

    # Find all matches of the regex in the output
    for match in tech_version_regex.finditer(output):
        tech, version = match.groups()
        # Some technologies might not have a version, handle these cases
        if version:
            tech_info[tech] = version
        else:
            tech_info[tech] = 'unknown version'

    return tech_info

def run_whatweb(domains, output_file='whatweb_output.json'):
    results = {}
    for domain in domains:
        try:
            # Run WhatWeb with the domain
            command = ['whatweb', '--color=never', '--no-errors', domain, 'a 1']
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            # Parse the WhatWeb output
            tech_info = parse_whatweb_output(result.stdout)
            results[domain] = tech_info
        except subprocess.CalledProcessError as e:
            print(f"Error running WhatWeb on {domain}: {e}")
            results[domain] = {"Error": str(e)}
        except Exception as e:
            print(f"Error processing WhatWeb output for {domain}: {e}")
            results[domain] = {"Error": "Processing Error"}

    # Save the results to a file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"Saved WhatWeb results to {output_file}")

# Example usage
if __name__ == "__main__":
    # Read subdomains from a file
    with open("subdomains.txt", "r") as file:
        domains = [line.strip() for line in file.readlines() if line.strip()]

    run_whatweb(domains)
