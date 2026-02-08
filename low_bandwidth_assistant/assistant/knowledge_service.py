"""
Knowledge Base Service
Handles local text file searching with intelligent keyword matching and scoring
"""

import re
from typing import List, Dict, Tuple
from django.conf import settings


class KnowledgeBaseService:
    def __init__(self):
        self.knowledge_data = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> List[Dict]:
        """
        Load and parse the knowledge base text file
        Format: Each entry should be:
        KEYWORDS: keyword1, keyword2, keyword3
        CONTENT: The actual information content
        ---
        """
        try:
            with open(settings.KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
                content = f.read()
            
            entries = []
            blocks = content.split('---')
            
            for block in blocks:
                block = block.strip()
                if not block:
                    continue
                
                lines = block.split('\n')
                keywords = []
                content_lines = []
                
                for line in lines:
                    if line.startswith('KEYWORDS:'):
                        keywords_str = line.replace('KEYWORDS:', '').strip()
                        keywords = [k.strip().lower() for k in keywords_str.split(',')]
                    elif line.startswith('CONTENT:'):
                        content_lines.append(line.replace('CONTENT:', '').strip())
                    elif content_lines:  # Continue content from previous line
                        content_lines.append(line.strip())
                
                if keywords and content_lines:
                    entries.append({
                        'keywords': keywords,
                        'content': ' '.join(content_lines)
                    })
            
            return entries
        except FileNotFoundError:
            return []
    
    def _calculate_relevance_score(self, query: str, entry: Dict) -> float:
        """
        Calculate how relevant an entry is to the query
        Uses keyword matching with scoring
        """
        query_lower = query.lower()
        query_words = set(re.findall(r'\w+', query_lower))
        
        score = 0.0
        matched_keywords = []
        
        # Check each keyword in the entry
        for keyword in entry['keywords']:
            keyword_lower = keyword.lower()
            
            # Exact keyword match in query (highest score)
            if keyword_lower in query_lower:
                score += 10.0
                matched_keywords.append(keyword)
            
            # Keyword appears as word in query
            elif keyword_lower in query_words:
                score += 8.0
                matched_keywords.append(keyword)
            
            # Partial match (keyword contains query word or vice versa)
            else:
                for query_word in query_words:
                    if len(query_word) > 3:  # Avoid matching very short words
                        if query_word in keyword_lower or keyword_lower in query_word:
                            score += 3.0
                            matched_keywords.append(keyword)
                            break
        
        # Bonus for multiple keyword matches (indicates better relevance)
        if len(matched_keywords) > 1:
            score += len(matched_keywords) * 2.0
        
        return score
    
    def search(self, query: str, max_results: int = 3) -> List[Tuple[Dict, float]]:
        """
        Search the knowledge base and return ranked results
        Returns list of (entry, score) tuples
        """
        results = []
        
        for entry in self.knowledge_data:
            score = self._calculate_relevance_score(query, entry)
            if score > 0:
                results.append((entry, score))
        
        # Sort by score (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:max_results]
    
    def get_best_match(self, query: str, min_score: float = 5.0) -> Dict:
        """
        Get the single best match for a query
        Returns None if no match meets minimum score
        """
        results = self.search(query, max_results=1)
        
        if results and results[0][1] >= min_score:
            return {
                'content': results[0][0]['content'],
                'score': results[0][1],
                'matched_keywords': results[0][0]['keywords'],
                'source': 'local'
            }
        
        return None
    
    def get_combined_response(self, query: str, max_entries: int = 2) -> Dict:
        """
        For multi-keyword queries, combine information from top matches
        """
        results = self.search(query, max_results=max_entries)
        
        if not results:
            return None
        
        # Combine content from top matches
        combined_content = []
        all_keywords = set()
        total_score = 0
        
        for entry, score in results:
            combined_content.append(entry['content'])
            all_keywords.update(entry['keywords'])
            total_score += score
        
        return {
            'content': ' '.join(combined_content),
            'score': total_score / len(results),  # Average score
            'matched_keywords': list(all_keywords),
            'source': 'local',
            'entries_combined': len(results)
        }
