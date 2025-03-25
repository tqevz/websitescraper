import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_file(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, os.path.basename(urlparse(url).path) or "index.html")
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")

def download_website(url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch the website.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    html_file = os.path.join(output_folder, "index.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
    print(f"Saved HTML: {html_file}")
    
    # Download CSS and JS files
    for tag in soup.find_all(["link", "script"]):
        src = tag.get("href") or tag.get("src")
        if src:
            file_url = urljoin(url, src)
            download_file(file_url, output_folder)

if __name__ == "__main__":
    website_url = input("Enter website URL: ")
    domain = urlparse(website_url).netloc.replace(".", "_")
    output_directory = os.path.join(os.getcwd(), domain)
    download_website(website_url, output_directory)
    print("Website decompiled successfully.")
