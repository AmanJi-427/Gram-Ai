# 🎯 QUICK START GUIDE

## ⚡ 3-Step Setup

### Step 1: Install Dependencies
```bash
cd low_bandwidth_assistant
pip install -r requirements.txt
```

### Step 2: Run the Server
```bash
python manage.py runserver
```

### Step 3: Open Browser
```
http://localhost:8000
```

---

## 📊 How Multi-Keyword Matching Works

```
USER QUERY: "What crops are best for summer weather?"
                         |
                         v
           ┌─────────────────────────┐
           │ Extract Keywords        │
           │ - crops                 │
           │ - summer                │
           │ - weather               │
           └───────────┬─────────────┘
                       |
                       v
           ┌─────────────────────────┐
           │ Search Knowledge Base   │
           │ Score all entries       │
           └───────────┬─────────────┘
                       |
        ┌──────────────┼──────────────┐
        v              v              v
   Entry 1         Entry 2        Entry 3
   Score: 24       Score: 10      Score: 8
   Keywords:       Keywords:      Keywords:
   summer ✓       weather ✓      crops ✓
   crops ✓
   hot
                       |
                       v
           ┌─────────────────────────┐
           │ Combine Top 2 Entries   │
           │ (Score 24 + Score 10)   │
           └───────────┬─────────────┘
                       |
                       v
               ┌───────────────┐
               │ COMBINED      │
               │ RESPONSE      │
               │ to User       │
               └───────────────┘
```

---

## 🎨 Project Architecture

```
┌────────────────────────────────────────┐
│         USER BROWSER                   │
│    (Minimal HTML/CSS/JS < 5KB)        │
└────────────┬───────────────────────────┘
             │
             v
┌────────────────────────────────────────┐
│         DJANGO SERVER                  │
│  ┌──────────────────────────────────┐ │
│  │      views.py (API Handler)      │ │
│  └───────────┬──────────────────────┘ │
│              │                         │
│    ┌─────────┴─────────┐              │
│    v                   v              │
│  ┌──────────────┐  ┌─────────────┐   │
│  │  Knowledge   │  │    Web      │   │
│  │  Base        │  │   Search    │   │
│  │  Service     │  │   Service   │   │
│  └──────┬───────┘  └──────┬──────┘   │
│         │                  │           │
└─────────┼──────────────────┼───────────┘
          │                  │
          v                  v
    ┌──────────┐      ┌──────────────┐
    │  Local   │      │  Internet    │
    │  data.txt│      │  (Fallback)  │
    └──────────┘      └──────────────┘
```

---

## 🔑 Key Files to Know

```
low_bandwidth_assistant/
│
├── 📄 manage.py                    → Run this to start server
│
├── ⚙️ settings.py                  → Configure MAX_RESPONSE_SIZE here
│
├── 🎯 assistant/
│   ├── views.py                   → Main request handler
│   ├── knowledge_service.py       → ⭐ SMART KEYWORD MATCHING
│   └── web_service.py             → Web fallback
│
├── 📚 knowledge_base/
│   └── data.txt                   → ⭐ ADD YOUR DATA HERE
│
├── 🎨 templates/
│   └── home.html                  → User interface
│
└── 📖 README.md                   → Full documentation
```

---

## ✏️ Adding New Knowledge

Edit `knowledge_base/data.txt`:

```
KEYWORDS: your, keywords, here, synonyms
CONTENT: The information you want to provide when users ask about these keywords.
---
```

**Example:**
```
KEYWORDS: rice, paddy, rice farming
CONTENT: Rice requires plenty of water and warm climate. Plant during monsoon season for best results.
---
```

---

## 🧪 Test Your Setup

Try these queries:

1. ✅ "What are summer crops?"
2. ✅ "crops for summer weather" (multi-keyword!)
3. ✅ "government schemes for farmers"
4. ✅ "How to calculate field area?"

---

## 🏆 Hackathon Demo Points

1. **Problem:** Rural areas need information with limited internet
2. **Solution:** Local knowledge base + smart matching
3. **Innovation:** Multi-keyword scoring algorithm
4. **Optimization:** <10KB responses, GZip compression
5. **Scalability:** Easy to add new knowledge domains
6. **Impact:** Works on 2G/3G connections

---

## 📞 Need Help?

Check these files:
- `README.md` - Full documentation
- `TESTING.md` - Detailed testing guide
- `knowledge_base/data.txt` - See example data format

---

**Built for low-bandwidth. Optimized for impact.** 🚀
