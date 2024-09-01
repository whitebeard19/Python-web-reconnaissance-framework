#! /usr/bin/python3

import json
import subprocess
from typing import Set

def read_input_json(file_path: str) -> dict:
    """
    Reads the input JSON from a file and returns it as a dictionary.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def extract_technologies(data: dict, include_list: Set[str]) -> Set[str]:
    """
    Extracts a set of unique technologies from the input JSON data,
    filtering based on an inclusion list.
    """
    technologies = set()
    for entry in data.values():
        for key in entry:
            if key in include_list:
                technologies.add(key)
    return technologies

def search_cves(technologies: Set[str], year: str = "2024") -> dict:
    """
    Searches for CVEs for the given technologies using the NIST CVE search tool,
    then processes the output with jq to extract CVE IDs and severities.
    """
    cve_results = {}
    for tech in technologies:
        try:
            command = f"python3 /home/whitebeard/tools/nist-cve-search-tool/tapir.py -y {year} {tech} | jq -r '.[]|[.cve.CVE_data_meta.ID,(.impact.baseMetricV2|if .severity == null then \"N/A\" else .severity end)]|@tsv'"
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            cve_results[tech] = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error searching CVEs for {tech}: {e}")
            cve_results[tech] = "Error"
    return cve_results

def format_cve_data(data, output_file: str):
    """
    Processes and prints the CVE search results in a human-readable format,
    then saves the original results to a JSON file.
    """
    for tech, cves in data.items():
        print(f"{tech}:")
        if cves:
            cve_list = cves.split('\n')
            for cve in cve_list:
                cve_id, severity = cve.split('\t')
                print(f"  - {cve_id} (Severity: {severity})")
        else:
            print("  - No CVEs found")
        print()  # Add a blank line for readability

    # Save the original results to a file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

#if __name__ == "__main__":
def main():
    input_file_path = "whatweb_output.json"  # Change this to the path of your input JSON file
    data = read_input_json(input_file_path)
    include_list = {"PHP", "JQuery", "Bootstrap"}  # Define the list of technologies you're interested in
    technologies = extract_technologies(data, include_list)
    cve_results = search_cves(technologies)
    format_cve_data(cve_results, "selected_technology_cves.json")

if __name__ == "__main__":
    main()
