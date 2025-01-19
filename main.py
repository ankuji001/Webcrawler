import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class SimpleWebCrawler:
    def _init_(self, base_url, max_pages=10):
        """
        Initializes the web crawler with a base URL and a maximum number of pages to crawl.

        :param base_url: The starting URL for the crawler.
        :param max_pages: The maximum number of pages to crawl.
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited = set()  # Set to keep track of visited URLs
        self.to_visit = [base_url]  # List of URLs to visit

    def crawl(self):
        """
        Starts the crawling process. It continues until there are no more pages to visit
        or the maximum number of pages has been reached.
        """
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)  # Get the next URL to visit
            if url in self.visited:
                continue  # Skip if already visited
            
            print(f"Crawling: {url}")
            self.visited.add(url)  # Mark the URL as visited
            self.get_links(url)  # Extract links from the current page
            time.sleep(1)  # Be polite and avoid overwhelming the server

    def get_links(self, url):
        """
        Fetches the content of the given URL and extracts all links from it.

        :param url: The URL to fetch and parse.
        """
        try:
            response = requests.get(url)  # Send a GET request to the URL
            response.raise_for_status()  # Raise an error for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')  # Parse the HTML content

            # Find all anchor tags with href attributes
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])  # Create a full URL
                # Check if the link is within the same domain and not already visited
                if self.base_url in full_url and full_url not in self.visited and full_url not in self.to_visit:
                    self.to_visit.append(full_url)  # Add the link to the list of URLs to visit
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")  # Handle request errors

if _name_ == "_main_":
    base_url = "https://example.com"  # Replace with the URL you want to crawl
    crawler = SimpleWebCrawler(base_url, max_pages=10)  # Create a crawler instance
    crawler.crawl()  # Start crawling