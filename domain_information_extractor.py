import requests
import whois
import colorama
from colorama import Fore
import argparse

def is_registered(domain_name):

    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def get_discovered_subdomains(domain, subdomain_list, timeout=2):
# List of discovered subdomains
    discovered_subdomains = []
    for subdomain in subdomain_list:
# Building the URL
        url = f"http://{subdomain}.{domain}"
        try:
# If this raises a connection error, that means the subdomain does not exist
            requests.get(url, timeout=timeout)
        except requests.ConnectionError:
# If the subdomain does not exist, just pass and print nothing on the screen
            pass
        else:
            print(Fore.RED + "[+] Discovered subdomain:", url)
# Update the discovered subdomain to our list
            discovered_subdomains.append(url)

    return discovered_subdomains

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Domain name information extractor uses the WHOIS database and scans for subdomains")
    parser.add_argument("domain", help="The domain name without http(s)")
    parser.add_argument("-t", "--timeout", type=int, default=2,
                        help="The timeout in seconds for prompting the connection, default is 2")
    parser.add_argument("-s", "--subdomains", default="subdomains.txt",
                        help="The file path that contains the list of subdomains to scan, default is subdomains.txt")
    parser.add_argument("-o", "--output",
                        help="The output file path resulting the discovered subdomains, default is {domain}-subdomains.txt")

# Parse the command-line arguments
    args = parser.parse_args()
    if is_registered(args.domain):
        whois_info = whois.whois(args.domain)
# Print the Registrar
        print(Fore.GREEN + "Domain Registrar:", whois_info.registrar)
# Print the WHOIS Server
        print(Fore.YELLOW + "WHOIS Server:", whois_info.whois_server)
# Get the Creation Date
        print(Fore.BLUE + "Domain Creation Date:", whois_info.creation_date)
# Get the Expiration Date
        print(Fore.MAGENTA + "Domain Expiration Date:", whois_info.expiration_date)
# Print the remaining information
        print(whois_info)

    print(Fore.CYAN + "."*50, "Scanning Subdomains", "."*50)
# Read all Subdomains
    with open(args.subdomains) as file:
# Read all Content
        content = file.read()
# Split by New Lines
        subdomains = content.splitlines()
    discovered_subdomains = get_discovered_subdomains(args.domain, subdomains)
# The Subdomain list filename will be named after the Domain name
    discovered_subdomains_file = f"{args.domain}-subdomains.txt"
# Save the discovered subdomains into a file so the information can be viewed again later without needing to run the scan again
    with open(discovered_subdomains_file, "w") as f:
        for subdomain in discovered_subdomains:
            print(subdomain, file=f)

from colorama import init
init(autoreset=True)
