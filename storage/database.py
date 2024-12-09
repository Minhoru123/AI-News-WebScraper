import sqlite3
from datetime import datetime


class AIInfoDatabase:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Research Papers Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS research_papers (
                id INTEGER PRIMARY KEY,
                title TEXT,
                authors TEXT,
                summary TEXT,
                link TEXT UNIQUE,
                category TEXT,
                published_date TEXT,
                scraped_at TEXT
            )
        ''')
        
        # News Articles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_articles (
                id INTEGER PRIMARY KEY,
                title TEXT,
                source TEXT,
                link TEXT UNIQUE,
                summary TEXT,
                category TEXT,
                scraped_at TEXT
            )
        ''')
        
        self.conn.commit()
    
    def insert_research_paper(self, paper):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO research_papers 
                (title, authors, summary, link, category, published_date, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                paper['title'],
                ', '.join(paper['authors']),
                paper['summary'],
                paper['link'],
                paper['category'],
                paper['published_date'],
                datetime.now().isoformat()
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate entries
            pass
    
    def insert_news_article(self, article):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO news_articles 
                (title, source, link, summary, category, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article.get('source', 'Unknown'),
                article['link'],
                article['summary'],
                ContentProcessor.categorize_content(article['summary']),
                datetime.now().isoformat()
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate entries
            pass
