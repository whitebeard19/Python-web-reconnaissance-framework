import asyncio
import httpx
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Step 1: Asynchronously check for live subdomains using httpx
async def check_subdomain(subdomain):
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"http://{subdomain}", follow_redirects=True)
            if response.status_code < 400:
                print(f"Live: {subdomain}")
                return subdomain
        except Exception as e:
            print(f"Error checking {subdomain}: {e}")
    return None

async def check_subdomains(subdomains):
    return await asyncio.gather(*(check_subdomain(subdomain) for subdomain in subdomains))

# Step 2: Spider the live subdomains using gau and waybackurls in parallel
def spider_subdomain(subdomain):
    spidered_urls = []
    try:
        #gau_output = subprocess.check_output(['gau', subdomain], text=True)
        wayback_output = subprocess.check_output(['waybackurls', subdomain], text=True)
        #spidered_urls.extend(gau_output.splitlines())
        spidered_urls.extend(wayback_output.splitlines())
    except subprocess.CalledProcessError as e:
        print(f"Error spidering {subdomain}: {e}")
    return spidered_urls

def spider_subdomains_in_parallel(live_subdomains):
    with ThreadPoolExecutor() as executor:
        spidered_urls = list(executor.map(spider_subdomain, live_subdomains))
    return [url for sublist in spidered_urls for url in sublist]  # Flatten the list

# Main function to orchestrate the steps
async def main():
    # Read subdomains from a file
    with open('subdomains.txt', 'r') as file:
        subdomains = file.read().splitlines()

    # Check for live subdomains
    live_subdomains = await check_subdomains(subdomains)
    live_subdomains = [subdomain for subdomain in live_subdomains if subdomain is not None]

    # Write live subdomains to a file
    with open('livesubdomains.txt', 'w') as file:
        for subdomain in live_subdomains:
            file.write(f"{subdomain}\n")

    # Spider the live subdomains in parallel
    spidered_urls = spider_subdomains_in_parallel(live_subdomains)

    # Write spidered URLs to a file
    with open('spidered_urls.txt', 'w') as file:
        for url in spidered_urls:
            file.write(f"{url}\n")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
