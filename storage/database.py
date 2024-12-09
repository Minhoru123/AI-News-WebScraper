# storage/database.py
import sqlite3
from datetime import datetime
import markdown2
import re


class AIInfoDatabase:

    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Enhanced table with more blog-friendly fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_content (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                source_link TEXT,
                content_type TEXT,  # research, news, blog, analysis
                tags TEXT,
                published_date TEXT,
                scraped_at TEXT,
                summary TEXT,
                reading_time INTEGER,
                complexity_level TEXT
            )
        ''')
        
        self.conn.commit()
    
    def calculate_reading_time(self, text):
        """
        Estimate reading time based on word count
        """
        words = len(re.findall(r'\w+', text))
        return max(1, words // 200)  # Assuming average reading speed
    
    def determine_complexity(self, text):
        """
        Assess content complexity
        """
        word_count = len(re.findall(r'\w+', text))
        syllable_count = len(re.findall(r'\w*[aeiou]\w*', text, re.IGNORECASE))
        
        if word_count < 300 and syllable_count < 100:
            return 'beginner'
        elif word_count < 600 and syllable_count < 200:
            return 'intermediate'
        else:
            return 'advanced'
    
    def insert_content(self, content_dict):
        """
        Insert content with enhanced metadata
        """
        cursor = self.conn.cursor()
        
        # Process content
        reading_time = self.calculate_reading_time(content_dict.get('content', ''))
        complexity = self.determine_complexity(content_dict.get('content', ''))
        
        # Generate summary if not provided
        summary = content_dict.get('summary', '')
        if not summary:
            summary = self.generate_summary(content_dict.get('content', ''))
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO ai_content 
                (title, content, source, source_link, content_type, 
                tags, published_date, scraped_at, summary, 
                reading_time, complexity_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content_dict.get('title', 'Untitled'),
                content_dict.get('content', ''),
                content_dict.get('source', 'Unknown'),
                content_dict.get('source_link', ''),
                content_dict.get('content_type', 'general'),
                ','.join(content_dict.get('tags', [])),
                content_dict.get('published_date', datetime.now().isoformat()),
                datetime.now().isoformat(),
                summary,
                reading_time,
                complexity
            ))
            self.conn.commit()
        except sqlite3.IntegrityError:
            # Handle duplicate entries
            pass
    
    def generate_summary(self, text, max_length=200):
        """
        Generate a brief summary of the content
        """
        # Remove markdown formatting
        plain_text = re.sub(r'[*_#\[\]]', '', text)
        
        # Truncate to max length
        summary = plain_text[:max_length]
        
        # Ensure we don't cut words mid-way
        summary = summary.rsplit(' ', 1)[0] + '...'
        
        return summary
    
    def get_blog_posts(self, limit=10, content_type=None, tag=None):
        """
        Retrieve blog-style posts with filtering options
        """
        cursor = self.conn.cursor()
        
        # Build query with optional filters
        query = "SELECT * FROM ai_content WHERE 1=1"
        params = []
        
        if content_type:
            query += " AND content_type = ?"
            params.append(content_type)
        
        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")
        
        query += " ORDER BY published_date DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return cursor.fetchall()
    
    def render_blog_post(self, post):
        """
        Convert database post to readable blog format
        """
        # Unpack post data
        _, title, content, source, source_link, content_type, tags, \
        published_date, _, summary, reading_time, complexity = post
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(content)
        
        # Create blog post template
        blog_post = f"""
# {title}

**Published:** {published_date}
**Source:** [{source}]({source_link})
**Reading Time:** {reading_time} min
**Complexity:** {complexity.capitalize()}
**Tags:** {tags}

## Summary
{summary}

## Full Content
{html_content}
"""
        return blog_post
    
    def export_to_markdown(self, output_dir='blog_posts'):
        """
        Export all posts to individual markdown files
        """
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all posts
        posts = self.get_blog_posts(limit=100)
        
        for post in posts:
            blog_post = self.render_blog_post(post)
            
            # Create filename from title
            filename = re.sub(r'[^\w\-_\. ]', '_', post[1])[:50] + '.md'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(blog_post)
