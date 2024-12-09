import logging
import schedule
import time
from config import Config
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


if __name__ == '__main__':
    main()
