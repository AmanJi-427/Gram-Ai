"""
Views for Low Bandwidth AI Assistant
Handles requests with bandwidth optimization
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json

from .knowledge_service import KnowledgeBaseService
from .web_service import WebSearchService


# Initialize services
kb_service = KnowledgeBaseService()
web_service = WebSearchService()


def home(request):
    """
    Render minimal homepage
    """
    return render(request, 'home.html', {
        'max_response_size': settings.MAX_RESPONSE_SIZE,
    })


@csrf_exempt
def api_query(request):
    """
    API endpoint for querying the assistant
    Optimized for minimal bandwidth usage
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if not query:
            return JsonResponse({'error': 'Query is required'}, status=400)
        
        # Track bandwidth usage
        response_data = {
            'query': query,
        }
        
        # Step 1: Search local knowledge base
        local_result = kb_service.get_combined_response(query, max_entries=2)
        
        if local_result and local_result['score'] >= 5.0:
            # Good local match found
            response_data.update({
                'answer': local_result['content'],
                'source': 'local',
                'matched_keywords': local_result.get('matched_keywords', []),
                'confidence': 'high' if local_result['score'] >= 15 else 'medium',
                'bytes': len(local_result['content']),
            })
        else:
            # No good local match - use web search fallback
            if settings.ENABLE_WEB_FALLBACK:
                web_result = web_service.search(query)
                response_data.update({
                    'answer': web_result['content'],
                    'source': 'web',
                    'confidence': 'low',
                    'bytes': web_result.get('bytes_used', len(web_result['content'])),
                    'fallback': True,
                })
            else:
                response_data.update({
                    'answer': 'No information available in local database. Web search is disabled.',
                    'source': 'none',
                    'confidence': 'none',
                    'bytes': 0,
                })
        
        # Enforce response size limit
        answer = response_data['answer']
        if len(answer) > settings.MAX_RESPONSE_SIZE:
            answer = answer[:settings.MAX_RESPONSE_SIZE - 50] + '... [truncated]'
            response_data['answer'] = answer
            response_data['truncated'] = True
        
        # Add metadata
        response_data['bytes'] = len(answer)
        response_data['kb_entries'] = len(kb_service.knowledge_data)
        
        return JsonResponse(response_data)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def stats(request):
    """
    Show system statistics
    """
    return JsonResponse({
        'knowledge_base_entries': len(kb_service.knowledge_data),
        'max_response_size_bytes': settings.MAX_RESPONSE_SIZE,
        'web_fallback_enabled': settings.ENABLE_WEB_FALLBACK,
    })
