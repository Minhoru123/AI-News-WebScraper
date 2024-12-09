import re


class ContentProcessor:

    @staticmethod
    def clean_text(text):
        """
        Clean and normalize text content
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        return text
    
    @staticmethod
    def categorize_content(content):
        """
        Basic content categorization
        """
        categories = {
            'research': ['paper', 'study', 'research', 'method', 'algorithm'],
            'product': ['product', 'launch', 'release', 'tool', 'platform'],
            'news': ['announcement', 'update', 'collaboration', 'partnership']
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in content.lower():
                    return category
        
        return 'general'
