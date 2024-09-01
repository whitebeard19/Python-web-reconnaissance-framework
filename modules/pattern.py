import subprocess
import sys

def use_gf_tool(url_file, pattern_type, output_file):
    try:
        with open(output_file, 'w') as file:
            result = subprocess.run(['gf', pattern_type, url_file], stdout=file, text=True)
    except FileNotFoundError:
        print(f"gf tool is not installed or not in PATH", file=sys.stderr)

def main():
    url_file = 'spidered_urls.txt'  # File containing URLs to check
    vulnerabilities = {
        'xss': 'urls_xss.txt',
        'sqli': 'urls_sqli.txt',
        'rce': 'urls_rce.txt'
    }

    for vuln_type, output_file in vulnerabilities.items():
        print(f"Finding potential {vuln_type.upper()} URLs...")
        use_gf_tool(url_file, vuln_type, output_file)
        print(f"Potential {vuln_type.upper()} URLs saved to {output_file}")

if __name__ == "__main__":
    main()
