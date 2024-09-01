import subprocess
import sys

def scan_for_xss():
    try:
        print(f"Scanning urls_xss for XSS vulnerabilities...")
        subprocess.run(['nuclei', '-list', 'urls_xss.txt', '-tags', 'xss'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while scanning: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("Nuclei is not installed or not in PATH", file=sys.stderr)

def scan_for_sqli(urls_file):
    try:
        print(f"Scanning {urls_file} for SQLi vulnerabilities...")
        subprocess.run(['nuclei', '-list', urls_file, '-tags', 'sqli'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while scanning: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("Nuclei is not installed or not in PATH", file=sys.stderr)

def scan_for_rce(urls_file):
    try:
        print(f"Scanning {urls_file} for RCE vulnerabilities...")
        subprocess.run(['nuclei', '-list', urls_file, '-tags', 'rce'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while scanning: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("Nuclei is not installed or not in PATH", file=sys.stderr)
