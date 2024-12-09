# scrapers/arxiv_scraper.py
import feedparser
import requests
from datetime import datetime, timedelta


class ArxivScraper:

    def __init__(self, config):
        self.config = config
    
    def scrape(self):
        papers = []
        for term in self.config.SOURCES['arxiv']['search_terms']:
            # Search for papers from the last 30 days
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
            # Construct search query
            search_query = f'ti:"{term}" AND submittedDate:[{start_date}000000 TO 999912312359]'
            
            # Make API request
            url = f'{self.config.SOURCES["arxiv"]["base_url"]}?search_query={search_query}&start=0&max_results=100'
            response = requests.get(url)
            
            # Parse XML response
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries:
                paper = {
                    'title': entry.title,
                    'authors': [author.name for author in entry.authors],
                    'summary': entry.summary,
                    'link': entry.link,
                    'published_date': entry.published,
                    'category': term
                }
                papers.append(paper)
        
        return papers
