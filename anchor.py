import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
from collections import deque

def is_internal_link(url, base_url):
    """Check if the link is internal to the base URL."""
    return urlparse(url).netloc == urlparse(base_url).netloc

def is_valid_url(url):
    """Check if the URL is valid for scraping."""
    # Reject URLs with # or ending with certain extensions
    invalid_extensions = ('.pdf', '.docx', '.doc', '.xlsx', '.xls', '.ppt', '.pptx', '.zip')
    if '#' in url or url.lower().endswith(invalid_extensions):
        return False
    return True

def scrape_content(url):
    """Fetch and return the BeautifulSoup object for the URL."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve {url} (status code: {response.status_code})")
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_anchor_tags(url, soup):
    """Extract anchor tag names and their corresponding URLs from the page."""
    anchor_tags = []
    a_tags = soup.find_all('a', href=True)
    
    for a_tag in a_tags:
        link = urljoin(url, a_tag['href'])  # Resolve relative URLs
        if is_internal_link(link, url) and is_valid_url(link):
            anchor_text = a_tag.get_text(strip=True)
            if anchor_text:  # Only include non-empty anchor texts
                anchor_tags.append({
                    "url": link,
                    "title": anchor_text
                })
    
    return anchor_tags

def scrape_website(url):
    """Scrape all internal pages starting from the base URL."""
    scraped_urls = set()  # Track scraped URLs to avoid duplication
    queue = deque([url])  # Queue for BFS
    data = []
    
    while queue:
        current_url = queue.popleft()
        
        if current_url in scraped_urls:
            continue
        
        print(f"Scraping URL: {current_url}")
        
        # Scrape the main page content and get soup object
        soup = scrape_content(current_url)
        if soup:  # Only add to data if content is successfully fetched
            # Find internal links and their anchor texts
            anchors = get_anchor_tags(current_url, soup)
                
            # Add the URL and its anchor tags to the data
            data.extend(anchors)

            # Enqueue internal links
            for anchor in anchors:
                link = anchor["url"]
                if link not in scraped_urls:
                    queue.append(link)
        
        scraped_urls.add(current_url)
    
    return data

def save_to_json(data, filename="output2.json"):
    """Save the scraped data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    url = "https://spo.iitk.ac.in"  # Replace with the URL you want to scrape
    scraped_data = scrape_website(url)
    save_to_json(scraped_data)
    print("Scraping complete. Data saved to output2.json.")
