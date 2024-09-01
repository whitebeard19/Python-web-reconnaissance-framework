#! /usr/bin/python3
import asyncio
import argparse
from modules import subdomain_collector,finge,cve,livespi,pattern,nuclei_scan

async def main():
    parser = argparse.ArgumentParser(description="WebHawk - A modular tool for subdomain enumeration, fingerprinting, CVE fetching, Vulnerability Pattern Matching, and Scaning for vulnerabilities using Nuclei Tool. ")
    parser.add_argument("-d", "--domain", help="Domain for subdomain enumeration")
    parser.add_argument("-m", "--module", help="Module to run: collect, fingerprint, cve, spider, pattern, nuclei ", choices=['collect', 'fingerprint', 'cve', 'spider', 'pattern', 'nuclei'])
    parser.add_argument("-t", "--type", help="specify the Type of vulnerabilities", choices=['xss', 'sqli', 'rce'])
    args = parser.parse_args()

    if args.module == 'collect' and args.domain:
        subdomain_collector.collect_subdomains(args.domain)
    elif args.module == 'fingerprint':
        finge.run_whatweb(args.domain)
    elif args.module == 'cve':
        cve.main()
    elif args.module == 'spider':
        await livespi.main()
    elif args.module == 'pattern':
        pattern.main()
    elif args.module == 'nuclei' and args.type == 'xss':
        nuclei_scan.scan_for_xss()
    else:
        print("Invalid module or missing domain for subdomain collection.")

if __name__ == "__main__":
    asyncio.run(main())
