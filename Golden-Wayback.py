import os
import requests
import re
from collections import defaultdict


print("""  
   _____       _     _                  _____                          
  / ____|     | |   | |                / ____|                         
 | |  __  ___ | | __| | ___ _ __ _____| (___   ___  ___ _   _ _ __ ___ 
 | | |_ |/ _ \| |/ _` |/ _ \ '_ \______\___ \ / _ \/ __| | | | '__/ _ \
 | |__| | (_) | | (_| |  __/ | | |     ____) |  __/ (__| |_| | | |  __/
  \_____|\___/|_|\__,_|\___|_| |_|    |_____/ \___|\___|\__,_|_|  \___|
                                                                       
                                                                       
                          Golden-Security  https://t.me/GoldenSecure                                                      
""")

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
        print(f"Saved: {filename} ({len(links)} links)")
    
    if email_links:
        with open(f"output/{domain}-emails.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(email_links))
        print(f"Saved: output/{domain}-emails.txt ({len(email_links)} links)")
    
    if sensitive_links:
        with open(f"output/{domain}-sensitive.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(sensitive_links))
        print(f"Saved: output/{domain}-sensitive.txt ({len(sensitive_links)} links)")

def main():
    domain = input("Enter domain: ").strip()
    print("Fetching data from Wayback Machine...")
    links = fetch_wayback_links(domain)
    if not links:
        print("No links found!")
        return
    
    print("Categorizing links...")
    categorized_links, email_links, sensitive_links = categorize_links(links)
    
    print("Saving links...")
    save_links(domain, categorized_links, email_links, sensitive_links)
    print("Process completed!")

if __name__ == "__main__":
    main()