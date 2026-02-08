# 🌐 Low Bandwidth AI Assistant - Django Hackathon Project

A Django-based AI assistant optimized for low-bandwidth internet connections. Uses local knowledge base with intelligent keyword matching and web search fallback.

## 🎯 Features

### ✅ Solved Problems

1. **Multi-Keyword Query Handling**
   - Smart scoring system ranks entries by relevance
   - Matches multiple keywords and combines results
   - Example: "crops for summer weather" matches both "crops" and "summer" keywords
   - Returns combined information from top matches

2. **Low Bandwidth Web Server**
   - GZip compression middleware enabled
   - Minimal HTML/CSS (< 5KB total)
   - Text-only interface, no images
   - Aggressive response size limiting

3. **Data Size Limits**
   - Maximum response: 10KB (configurable)
   - Web searches limited to top 3 results
   - Automatic content truncation
   - Bandwidth usage tracking

## 🏗️ Architecture

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Django Frontend    │  (Minimal HTML/CSS)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Knowledge Base     │  ──► Local Search (Priority 1)
│  Service            │      - Keyword matching
└──────────┬──────────┘      - Relevance scoring
           │                 - Multi-keyword support
           │
           ▼ (if no match)
┌─────────────────────┐
│  Web Search Service │  ──► Internet Fallback (Priority 2)
│                     │      - DuckDuckGo Lite
└─────────────────────┘      - Size-limited downloads
```

## 📁 Project Structure

```
low_bandwidth_assistant/
├── manage.py                 # Django management script
├── settings.py              # Django settings with bandwidth optimizations
├── urls.py                  # URL routing
├── wsgi.py                  # WSGI application
├── requirements.txt         # Python dependencies
├── assistant/               # Main app
│   ├── views.py            # Request handlers with optimization
│   ├── knowledge_service.py # Smart keyword matching engine
│   └── web_service.py      # Web search fallback
├── templates/
│   └── home.html           # Ultra-minimal interface
├── static/css/
│   └── style.css           # Compressed CSS (< 2KB)
└── knowledge_base/
    └── data.txt            # Local knowledge database
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Run Migrations (if needed)

```bash
python manage.py migrate
```

### 3. Start the Server

```bash
python manage.py runserver
```

### 4. Access the Application

Open your browser and go to: `http://localhost:8000`

## 📝 Knowledge Base Format

The knowledge base uses a simple text format in `knowledge_base/data.txt`:

```
KEYWORDS: keyword1, keyword2, keyword3
CONTENT: Your information content here. Can span multiple lines.
---
KEYWORDS: another, set, of, keywords
CONTENT: More information here.
---
```

### Example Entry:

```
KEYWORDS: summer crops, hot weather, kharif
CONTENT: Best crops for summer include pearl millet, sorghum, and groundnut. These are drought-resistant and suitable for high temperatures.
---
```

## 🎮 How It Works

### Multi-Keyword Query Example:

**User asks:** "What crops are best for summer weather?"

**System Process:**
1. Extracts keywords: "crops", "summer", "weather"
2. Scores all entries:
   - Entry with "summer crops" → Score: 18 (2 keywords matched)
   - Entry with "weather" → Score: 10 (1 keyword matched)
   - Entry with "crops" → Score: 10 (1 keyword matched)
3. Combines top 2 entries
4. Returns combined response with metadata

### Scoring Algorithm:
- Exact keyword match in query: **+10 points**
- Keyword as word in query: **+8 points**
- Partial match: **+3 points**
- Multiple keyword bonus: **+2 points per additional keyword**

## ⚙️ Configuration

Edit `settings.py` to customize:

```python
# Maximum response size (bytes)
MAX_RESPONSE_SIZE = 10240  # 10KB

# Knowledge base location
KNOWLEDGE_BASE_PATH = BASE_DIR / 'knowledge_base' / 'data.txt'

# Enable/disable web fallback
ENABLE_WEB_FALLBACK = True

# Web search timeout (seconds)
WEB_SEARCH_TIMEOUT = 5
```

## 🧪 Testing the System

### Test 1: Local Knowledge Base
```
Query: "What are summer crops?"
Expected: Returns local data about summer crops
Source: LOCAL
```

### Test 2: Multi-Keyword
```
Query: "crops for summer weather"
Expected: Combines info from "crops", "summer", and "weather" entries
Source: LOCAL (combined)
```

### Test 3: Web Fallback
```
Query: "latest technology news"
Expected: Uses web search (no local match)
Source: WEB
```

### Test 4: Arithmetic
```
Query: "how to calculate field area"
Expected: Returns arithmetic and measurement info
Source: LOCAL
```

## 📊 Bandwidth Optimization Features

1. **GZip Compression** - Automatically compresses all responses
2. **Minimal Frontend** - Only 5KB HTML+CSS combined
3. **Text-Only** - No images, icons loaded via emoji
4. **Size Limiting** - All responses capped at 10KB
5. **Lazy Loading** - Only fetches what's needed
6. **Caching** - Static files cached by browser
7. **Stream Control** - Web downloads stopped at size limit

## 🔧 Extending the Knowledge Base

Add new entries to `knowledge_base/data.txt`:

```
KEYWORDS: your, keywords, here
CONTENT: Your information content
---
```

**Tips for Good Keywords:**
- Use specific terms users might search for
- Include synonyms and related terms
- Add plural and singular forms
- Mix general and specific keywords

## 🐛 Troubleshooting

**Issue**: No local matches found
- **Solution**: Add more keywords to your knowledge base entries

**Issue**: Web search not working
- **Solution**: Check internet connection, or disable web fallback in settings

**Issue**: Responses too large
- **Solution**: Reduce `MAX_RESPONSE_SIZE` in settings.py

**Issue**: Slow performance
- **Solution**: Reduce `WEB_SEARCH_TIMEOUT` or disable web fallback

## 🎓 Hackathon Presentation Points

1. **Problem Solved**: Low-bandwidth internet access in rural areas
2. **Smart Matching**: Multi-keyword relevance scoring system
3. **Bandwidth Optimized**: <10KB responses, GZip compression
4. **Dual Source**: Local knowledge + web fallback
5. **Scalable**: Easy to add new knowledge domains
6. **User-Friendly**: Simple, minimal interface

## 📈 Future Enhancements

- [ ] Add caching layer for web searches
- [ ] Implement user analytics dashboard
- [ ] Add voice input for low-literacy users
- [ ] Mobile app version
- [ ] Offline mode with service workers
- [ ] Multi-language support
- [ ] SMS/USSD interface for feature phones

## 📄 License

Open source - feel free to use and modify for your hackathon!

## 👥 Team

Your team name and members here

---

**Built for low-bandwidth regions. Optimized for impact.** 🚀
