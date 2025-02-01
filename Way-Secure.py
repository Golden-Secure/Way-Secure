import os
import requests
import re
from collections import defaultdict
from colorama import Fore, Back, Style, init

init(autoreset=True)

print(Fore.GREEN + """

██     ██  █████  ██    ██       ███████ ███████  ██████ ██    ██ ██████  ███████ 
██     ██ ██   ██  ██  ██        ██      ██      ██      ██    ██ ██   ██ ██      
██  █  ██ ███████   ████   █████ ███████ █████   ██      ██    ██ ██████  █████   
██ ███ ██ ██   ██    ██               ██ ██      ██      ██    ██ ██   ██ ██      
 ███ ███  ██   ██    ██          ███████ ███████  ██████  ██████  ██   ██ ███████                                                                                                 
                          Golden-Security  https://t.me/GoldenSecure
""" + Style.RESET_ALL)


def fetch_wayback_links(domain):
    url = f"https://web.archive.org/cdx/search/cdx?url=*.{domain}/*&collapse=urlkey&output=text&fl=original"
    response = requests.get(url)
    if response.status_code == 200:
        return list(set(response.text.splitlines()))  # Remove duplicates
    return []


def categorize_links(links):
    file_extensions = re.compile(r'.*\.(xls|xml|xlsx|json|pdf|sql|doc|docx|pptx|txt|zip|tar\.gz|tgz|bak|7z|rar|log|cache|secret|db|backup|yml|gz|git|config|csv|yaml|md|md5|exe|dll|bin|ini|bat|sh|tar|deb|rpm|iso|img|apk|msi|env|dmg|tmp|crt|pem|key|pub|asc)$', re.IGNORECASE)
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    sensitive_pattern = re.compile(r'(internal use only|confidential|strictly private|personal & confidential|private|restricted|internal|not for distribution|do not share|proprietary|trade secret|classified|sensitive|bank statement|invoice|salary|contract|agreement|non disclosure|passport|social security|ssn|date of birth|credit card|identity|id number|company confidential|staff only|management only|internal only)', re.IGNORECASE)
    
    categorized = defaultdict(list)
    email_links = []
    sensitive_links = []
    
    for link in links:
        if email_pattern.search(link):
            email_links.append(link)
        if sensitive_pattern.search(link):
            sensitive_links.append(link)
        match = file_extensions.search(link)
        if match:
            ext = match.group(1).lower()
            categorized[ext].append(link)
    
    return categorized, email_links, sensitive_links


def save_links(domain, categorized_links, email_links, sensitive_links):
    if not os.path.exists("output"):
        os.makedirs("output")
    
    for ext, links in categorized_links.items():
        filename = f"output/{domain}-{ext}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(links))
        print(Fore.CYAN + f"Saved: {filename} ({len(links)} links)" + Style.RESET_ALL)
    
    if email_links:
        with open(f"output/{domain}-emails.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(email_links))
        print(Fore.YELLOW + f"Saved: output/{domain}-emails.txt ({len(email_links)} links)" + Style.RESET_ALL)
    
    if sensitive_links:
        with open(f"output/{domain}-sensitive.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(sensitive_links))
        print(Fore.RED + f"Saved: output/{domain}-sensitive.txt ({len(sensitive_links)} links)" + Style.RESET_ALL)


def main():
    domain = input(Fore.GREEN + "Enter domain: " + Style.RESET_ALL).strip()
    print(Fore.GREEN + "Fetching data from Wayback Machine..." + Style.RESET_ALL)
    links = fetch_wayback_links(domain)
    if not links:
        print(Fore.RED + "No links found!" + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + "Categorizing links..." + Style.RESET_ALL)
    categorized_links, email_links, sensitive_links = categorize_links(links)
    
    print(Fore.GREEN + "Saving links..." + Style.RESET_ALL)
    save_links(domain, categorized_links, email_links, sensitive_links)
    print(Fore.GREEN + "Process completed!" + Style.RESET_ALL)


if __name__ == "__main__":
    main()
