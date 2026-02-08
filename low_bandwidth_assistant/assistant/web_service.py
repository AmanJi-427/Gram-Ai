"""
Web Search Fallback Service
Ultra-lightweight web search for when local knowledge base has no match
Optimized for low bandwidth
"""

import requests
from typing import Dict
from bs4 import BeautifulSoup
from django.conf import settings


class WebSearchService:
    def __init__(self):
        self.timeout = getattr(settings, 'WEB_SEARCH_TIMEOUT', 5)
        self.max_response_size = getattr(settings, 'MAX_RESPONSE_SIZE', 10240)
    
    def search(self, query: str) -> Dict:
        """
        Perform a lightweight web search and extract minimal text
        Returns summarized content optimized for low bandwidth
        """
        try:
            # Use DuckDuckGo Lite (text-only, minimal bandwidth)
            search_url = f"https://lite.duckduckgo.com/lite/?q={requests.utils.quote(query)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; LowBandwidthBot/1.0)'
            }
            
            response = requests.get(
                search_url, 
                headers=headers, 
                timeout=self.timeout,
                stream=True  # Stream to control download size
            )
            
            # Read only up to max size
            content = b''
            downloaded = 0
            chunk_size = 1024
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                content += chunk
                downloaded += len(chunk)
                if downloaded >= self.max_response_size:
                    break
            
            # Parse minimal HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract search result snippets (text only)
            results = []
            for result in soup.find_all('td', class_='result-snippet')[:3]:  # Top 3 results
                text = result.get_text(strip=True)
                if text:
                    results.append(text)
            
            # If no snippets, try to get any text content
            if not results:
                text_elements = soup.find_all('p')[:5]
                results = [p.get_text(strip=True) for p in text_elements if p.get_text(strip=True)]
            
            if results:
                # Combine and limit size
                combined = ' '.join(results)
                # Limit to reasonable size (5KB of text)
                if len(combined) > 5000:
                    combined = combined[:5000] + '...'
                
                return {
                    'content': combined,
                    'source': 'web',
                    'query': query,
                    'bytes_used': len(combined)
                }
            
            return {
                'content': 'No web results found. Please try a different query.',
                'source': 'web',
                'query': query,
                'bytes_used': 0
            }
            
        except requests.Timeout:
            return {
                'content': 'Search timeout - connection too slow. Try again later.',
                'source': 'web',
                'error': 'timeout'
            }
        except Exception as e:
            return {
                'content': f'Web search unavailable. Using local knowledge only.',
                'source': 'web',
                'error': str(e)
            }
    
    def get_simple_answer(self, query: str) -> str:
        """
        Get a simple text answer optimized for bandwidth
        """
        result = self.search(query)
        return result.get('content', 'No information available.')
