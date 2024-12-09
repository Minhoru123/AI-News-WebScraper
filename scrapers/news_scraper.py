# Updated news_scraper.py
import requests
from bs4 import BeautifulSoup
import logging
import random


class NewsScraper:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # User Agent rotation to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
    
    def get_headers(self):
        """
        Generate random headers to mimic browser request
        """
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def scrape_venturebeat(self, url):
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            # More comprehensive selector for VentureBeat
            article_elements = soup.find_all(['article', 'div'], class_=['article', 'article-content', 'post'])
            
            for article in article_elements:
                title_elem = article.find(['h2', 'h3', 'h1'], class_=['article-title', 'title'])
                link_elem = article.find('a', href=True)
                summary_elem = article.find(['p', 'div'], class_=['article-excerpt', 'excerpt'])
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem['href']
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    articles.append({
                        'source': 'VentureBeat',
                        'title': title,
                        'link': link,
                        'summary': summary
                    })
            
            return articles
        
        except Exception as e:
            self.logger.error(f"Error scraping VentureBeat {url}: {e}")
            return []
    
    def scrape_techcrunch(self, url):
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            # TechCrunch specific selectors
            article_elements = soup.find_all('div', class_=['post-block'])
            
            for article in article_elements:
                title_elem = article.find('h2', class_=['post-block__title'])
                link_elem = article.find('a', href=True)
                summary_elem = article.find('div', class_=['post-block__content'])
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = link_elem['href']
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    articles.append({
                        'source': 'TechCrunch',
                        'title': title,
                        'link': link,
                        'summary': summary
                    })
            
            return articles
        
        except Exception as e:
            self.logger.error(f"Error scraping TechCrunch {url}: {e}")
            return []
    
    def scrape_wired(self, url):
        try:
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            # Wired specific selectors
            article_elements = soup.find_all('div', class_=['content-list-item'])
            
            for article in article_elements:
                title_elem = article.find('h2')
                link_elem = article.find('a', href=True)
                summary_elem = article.find('p', class_=['summary'])
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    link = 'https://www.wired.com' + link_elem['href']
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    articles.append({
                        'source': 'Wired',
                        'title': title,
                        'link': link,
                        'summary': summary
                    })
            
            return articles
        
        except Exception as e:
            self.logger.error(f"Error scraping Wired {url}: {e}")
            return []
    
    def scrape(self):
        all_articles = []
        
        # Source-specific scraping methods
        scraping_methods = {
            'https://venturebeat.com/category/ai/': self.scrape_venturebeat,
            'https://techcrunch.com/category/artificial-intelligence/': self.scrape_techcrunch,
            'https://www.wired.com/category/gear/artificial-intelligence/': self.scrape_wired
        }
        
        for source_url, scrape_method in scraping_methods.items():
            try:
                articles = scrape_method(source_url)
                all_articles.extend(articles)
            except Exception as e:
                self.logger.error(f"Error scraping {source_url}: {e}")
        
        return all_articles
