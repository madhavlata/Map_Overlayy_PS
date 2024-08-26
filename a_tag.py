import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
from collections import deque
import re

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
    """Fetch and return the text content of the URL and the BeautifulSoup object."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text(separator=" ", strip=True)
            return content, soup
        else:
            print(f"Failed to retrieve {url} (status code: {response.status_code})")
            return "", None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return "", None

def get_anchor_text(soup):
    """Extract the first anchor tag text or use the page title if no anchor tags are found."""
    a_tag = soup.find('a', href=True)
    if a_tag:
        anchor_text = a_tag.get_text(strip=True)
        if anchor_text:
            return anchor_text
    
    title = soup.title.string if soup.title and soup.title.string.strip() else 'No Title'
    return title

def extract_links(soup, base_url):
    """Extract all internal links from the page content, including from buttons."""
    links = []

    # Extract links from anchor tags
    for a_tag in soup.find_all('a', href=True):
        link = urljoin(base_url, a_tag['href'])  # Resolve relative URLs
        if is_internal_link(link, base_url) and is_valid_url(link):
            links.append(link)
    
    # Extract links from buttons (or elements that may redirect)
    for button in soup.find_all(['button', 'a'], href=True):
        if button.name == 'a':  # 'a' tag used as a button
            link = urljoin(base_url, button['href'])
            if is_internal_link(link, base_url) and is_valid_url(link):
                links.append(link)
        elif button.name == 'button':  # 'button' tag might not have href but could be used for navigation
            onclick = button.get('onclick', '')
            match = re.search(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", onclick)
            if match:
                link = urljoin(base_url, match.group(1))
                if is_internal_link(link, base_url) and is_valid_url(link):
                    links.append(link)

    # Extract links from JavaScript within the page
    scripts = soup.find_all('script')
    for script in scripts:
        if script.string:
            # Search for window.location.href or similar JS redirections
            matches = re.findall(r"window\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", script.string)
            for match in matches:
                link = urljoin(base_url, match)
                if is_internal_link(link, base_url) and is_valid_url(link):
                    links.append(link)

            # Capture potential AJAX or dynamic URL loading
            ajax_matches = re.findall(r"\$.ajax\(\{.*?url\s*:\s*['\"]([^'\"]+)['\"]", script.string, re.DOTALL)
            for match in ajax_matches:
                link = urljoin(base_url, match)
                if is_internal_link(link, base_url) and is_valid_url(link):
                    links.append(link)

    # Extract links from form actions
    for form in soup.find_all('form'):
        action = form.get('action')
        if action:
            link = urljoin(base_url, action)
            if is_internal_link(link, base_url) and is_valid_url(link):
                links.append(link)

    return list(set(links))  # Return unique internal links

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
        content, soup = scrape_content(current_url)
        if content and soup:  # Only add to data if content is not empty
            # Find the anchor text
            anchor_text = get_anchor_text(soup)
                
            # Add the URL and its content along with the anchor text
            data.append({
                "url": current_url,
                "content": content,
                "title": anchor_text
            })

            # Enqueue internal links
            internal_links = extract_links(soup, current_url)
            for link in internal_links:
                if link not in scraped_urls:
                    queue.append(link)
        
        scraped_urls.add(current_url)
    
    return data

def save_to_json(data, filename="output1.json"):
    """Save the scraped data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    url = "https://spo.iitk.ac.in/"  # Replace with the URL you want to scrape
    scraped_data = scrape_website(url)
    save_to_json(scraped_data)
    print("Scraping complete. Data saved to output1.json.")
