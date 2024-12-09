import requests
from bs4 import BeautifulSoup
import logging


class NewsScraper:

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def scrape_source(self, url):
        try:
            response = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            articles = []
            
            # VentureBeat-style scraping
            if 'venturebeat' in url:
                article_elements = soup.find_all('article', class_='article-content')
                for article in article_elements:
                    title = article.find('h2').text.strip()
                    link = article.find('a')['href']
                    summary = article.find('div', class_='article-excerpt').text.strip()
                    
                    articles.append({
                        'source': 'VentureBeat',
                        'title': title,
                        'link': link,
                        'summary': summary
                    })
            
            # Add more source-specific parsing as needed
            
            return articles
        
        except Exception as e:
            self.logger.error(f"Error scraping {url}: {e}")
            return []

    def scrape(self):
        all_articles = []
        for source_url in self.config.SOURCES['news_sources']:
            articles = self.scrape_source(source_url)
            all_articles.extend(articles)
        return all_articles
