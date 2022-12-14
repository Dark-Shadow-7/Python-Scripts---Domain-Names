import requests
from threading import Thread, Lock
from queue import Queue

q = Queue()
list_lock = Lock()
discovered_domains = []

def scan_subdomains(domain):
    global q
    while True:
#Obtain the Subdomain from the Queue
        subdomain = q.get()
#Scan the Subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            requests.get(url)
        except requests.ConnectionError:
            pass
        else:
            print("[+] Discovered subdomain:", url)
#Add the Subdomain to the Global List
            with list_lock:
                discovered_domains.append(url)
#Scanning that Subdomain is complete
        q.task_done()

def main(domain, n_threads, subdomains):
    global q

#Populate the Queue with all the discovered Subdomains
    for subdomain in subdomains:
        q.put(subdomain)

    for t in range(n_threads):
#Begin the threads
        worker = Thread(target=scan_subdomains, args=(domain,))
#Daemon thread means that a thread will end when the main thread is done
        worker.daemon = True
        worker.start()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Faster Subdomain Scanner using Threads")
    parser.add_argument("domain", help="Domain to scan for subdomains without protocol (e.g without 'http://' or 'https://')")
    parser.add_argument("-l", "--wordlist", help="File that contains all subdomains to scan, line by line. Default is subdomains.txt",
                        default="subdomains.txt")
    parser.add_argument("-t", "--num-threads", help="Number of threads to use to scan the domain. Default is 10", default=10, type=int)
    parser.add_argument("-o", "--output-file", help="Specify the output text file to write discovered subdomains", default="discovered-subdomains.txt")
    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    num_threads = args.num_threads
    output_file = args.output_file

    main(domain=domain, n_threads=num_threads, subdomains=open(wordlist).read().splitlines())
    q.join()

#Save the discovered Subdomains to a file
    with open(output_file, "w") as f:
        for url in discovered_domains:
            print(url, file=f)
