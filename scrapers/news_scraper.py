import requests
from bs4 import BeautifulSoup
import logging
import random
import traceback


class NewsScraper:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Expanded logging for debugging
        self.detailed_logger = logging.getLogger('news_scraper_detailed')
        handler = logging.FileHandler('news_scraper_debug.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s:\n%(message)s\n')
        handler.setFormatter(formatter)
        self.detailed_logger.addHandler(handler)
        self.detailed_logger.setLevel(logging.DEBUG)

    def debug_log(self, url, response=None, exception=None):
        """
        Comprehensive logging for debugging scraping issues
        """
        log_entry = f"""
DEBUG LOG FOR: {url}
-------------------
Response Status: {response.status_code if response else 'No Response'}
Response Headers: {dict(response.headers) if response else 'No Headers'}
"""
        if exception:
            log_entry += f"\nException Details:\n{traceback.format_exc()}"
        
        if response:
            # Log first 1000 characters of content
            log_entry += f"\nResponse Content Preview:\n{response.text[:1000]}"
        
        self.detailed_logger.debug(log_entry)

    def scrape_venturebeat(self, url):
        try:
            # Enhanced request with more comprehensive headers
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            # Log response for debugging
            self.debug_log(url, response)
            
            # Check for successful response
            if response.status_code != 200:
                self.logger.warning(f"Non-200 status code for {url}: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            # Multiple selector strategies
            selector_strategies = [
                {'tags': ['article'], 'classes': ['article', 'article-content', 'post']},
                {'tags': ['div'], 'classes': ['article-wrapper', 'post-block']},
            ]

            for strategy in selector_strategies:
                article_elements = soup.find_all(strategy['tags'], class_=strategy['classes'])
                
                for article in article_elements:
                    title_elem = article.find(['h2', 'h3', 'h1'], class_=['article-title', 'title', 'post-title'])
                    link_elem = article.find('a', href=True)
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text(strip=True)
                        link = link_elem['href']
                        
                        # Ensure absolute URL
                        if not link.startswith(('http://', 'https://')):
                            link = f'https://venturebeat.com{link}'
                        
                        articles.append({
                            'source': 'VentureBeat',
                            'title': title,
                            'link': link,
                            'summary': ''  # You might want to extract summary if possible
                        })
                
                # If articles found, break the strategy loop
                if articles:
                    break
            
            self.logger.info(f"Scraped {len(articles)} articles from VentureBeat")
            return articles
        
        except Exception as e:
            self.debug_log(url, exception=e)
            self.logger.error(f"Complete error scraping VentureBeat {url}: {e}")
            return []

    def scrape(self):
        all_articles = []
        
        # Focus on VentureBeat for now
        sources = ['https://venturebeat.com/category/ai/']
        
        for source_url in sources:
            try:
                articles = self.scrape_venturebeat(source_url)
                all_articles.extend(articles)
            except Exception as e:
                self.logger.error(f"Error processing {source_url}: {e}")
        
        return all_articles
