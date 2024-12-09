import os


class Config:
    # Scraping Sources
    SOURCES = {
        'arxiv': {
            'base_url': 'http://export.arxiv.org/api/query',
            'search_terms': [
                'artificial intelligence',
                'machine learning',
                'deep learning',
                'natural language processing',
                'computer vision'
            ]
        },
        'news_sources': [
            'https://venturebeat.com/category/ai/',
            'https://techcrunch.com/category/artificial-intelligence/',
            'https://www.wired.com/category/gear/artificial-intelligence/'
        ],
        'tech_blogs': [
            'https://ai.googleblog.com/',
            'https://openai.com/blog',
            'https://deepmind.com/blog'
        ]
    }

    # Storage Configuration
    DATABASE_PATH = 'ai_info_database.sqlite'
    
    # Logging
    LOG_FILE = 'ai_scraper.log'
