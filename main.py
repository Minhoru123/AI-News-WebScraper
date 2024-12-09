import logging
import schedule
import time
from config import Config
from datetime import datetime
from scrapers.arxiv_scraper import ArxivScraper
from scrapers.news_scraper import NewsScraper
from storage.database import AIInfoDatabase


def setup_logging():
    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Initialize database
    database = AIInfoDatabase(Config.DATABASE_PATH)
    
    def scrape_job():
        try:
            # Scrape research papers
            arxiv_scraper = ArxivScraper(Config)
            research_papers = arxiv_scraper.scrape()
            for paper in research_papers:
                database.insert_research_paper(paper)
            
            # Scrape news articles
            news_scraper = NewsScraper(Config)
            news_articles = news_scraper.scrape()
            for article in news_articles:
                database.insert_news_article(article)
            
            logger.info(f"Scraped {len(research_papers)} research papers and {len(news_articles)} news articles")
        
        except Exception as e:
            logger.error(f"Scraping job failed: {e}")
    
    # Run immediately
    scrape_job()
    
    # Schedule job to run daily
    schedule.every().day.at("09:00").do(scrape_job)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)


# Update main.py to use new database method
def update_main_scrape_method():
    """
    Modify scraping methods to use new database insert
    """

    # For ArXiv scraper
    def process_arxiv_paper(paper):
        return {
            'title': paper['title'],
            'content': f"""
# {paper['title']}

**Authors:** {', '.join(paper['authors'])}

## Abstract
{paper['summary']}

## Details
- Link: {paper['link']}
- Category: {paper['category']}
""",
            'source': 'ArXiv',
            'source_link': paper['link'],
            'content_type': 'research',
            'tags': ['AI', paper['category']],
            'published_date': paper.get('published_date', datetime.now().isoformat())
        }

    # For News scraper
    def process_news_article(article):
        return {
            'title': article['title'],
            'content': f"""
# {article['title']}

## Article Summary
{article.get('summary', '')}

## Full Details
- Source: {article['source']}
- Link: {article['link']}
""",
            'source': article['source'],
            'source_link': article['link'],
            'content_type': 'news',
            'tags': ['AI', article['source']],
            'published_date': datetime.now().isoformat()
        }


if __name__ == '__main__':
    main()
