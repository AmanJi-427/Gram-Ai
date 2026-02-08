# 🧪 Testing Guide for Low Bandwidth AI Assistant

## Quick Test Queries

### 1. Single Keyword Queries (Local DB)

**Query:** "What is weather?"
- **Expected Result:** Information about weather from local KB
- **Source:** LOCAL
- **Keywords Matched:** weather

**Query:** "Tell me about crops"
- **Expected Result:** Information about farming and crops
- **Source:** LOCAL
- **Keywords Matched:** crops, farming, agriculture

**Query:** "irrigation methods"
- **Expected Result:** Information about irrigation
- **Source:** LOCAL
- **Keywords Matched:** irrigation, water

---

### 2. Multi-Keyword Queries (The Challenge!)

**Query:** "What crops are best for summer weather?"
- **Expected Result:** Combined information from "summer crops" AND "weather" entries
- **Source:** LOCAL
- **Keywords Matched:** summer, crops, weather
- **Score:** High (multiple keyword matches)
- **Behavior:** System combines info from top 2 relevant entries

**Query:** "government schemes for farmers"
- **Expected Result:** Information about government support and subsidies
- **Source:** LOCAL
- **Keywords Matched:** government, scheme, farmer

**Query:** "How to store harvested crops?"
- **Expected Result:** Combined info from "harvest" and "storage" entries
- **Source:** LOCAL
- **Keywords Matched:** storage, harvest, crops

---

### 3. Arithmetic and Calculations

**Query:** "How do I calculate land area?"
- **Expected Result:** Information about arithmetic and area measurement
- **Source:** LOCAL
- **Keywords Matched:** arithmetic, area, measurement

**Query:** "What is addition and subtraction?"
- **Expected Result:** Basic arithmetic operations info
- **Source:** LOCAL
- **Keywords Matched:** arithmetic, math, addition, subtraction

---

### 4. Web Fallback Tests

**Query:** "latest cricket scores"
- **Expected Result:** Web search results (not in local KB)
- **Source:** WEB
- **Fallback:** True

**Query:** "current news today"
- **Expected Result:** Web search results
- **Source:** WEB
- **Fallback:** True

---

## Testing the Scoring System

### Example: "summer weather crops"

**Entry 1: "summer crops"**
- Keywords: summer, crops, kharif, hot
- Matches: summer ✓, crops ✓
- Score: 10 + 10 + 4 (multi-keyword bonus) = **24 points**

**Entry 2: "weather"**
- Keywords: weather, forecast, temperature
- Matches: weather ✓
- Score: **10 points**

**Entry 3: "crops"**
- Keywords: crops, farming, agriculture
- Matches: crops ✓
- Score: **10 points**

**Result:** Top 2 entries (24 + 10 points) get combined

---

## Bandwidth Usage Tests

### Test Response Sizes

**Query:** "Tell me everything about farming"
- Check that response is under 10KB
- Verify "bytes" field in API response

**Query:** Very specific question requiring web search
- Check "bytes_used" from web search
- Verify download was limited

---

## API Testing (using curl)

```bash
# Test basic query
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "summer crops"}'

# Test multi-keyword query
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "crops for summer weather"}'

# Test web fallback
curl -X POST http://localhost:8000/api/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "latest technology news"}'
```

---

## Expected API Response Format

```json
{
  "query": "crops for summer weather",
  "answer": "Combined content from matching entries...",
  "source": "local",
  "matched_keywords": ["summer", "crops", "weather"],
  "confidence": "high",
  "bytes": 486,
  "kb_entries": 20,
  "entries_combined": 2
}
```

---

## Edge Cases to Test

### 1. Empty Query
**Query:** ""
- **Expected:** Error message "Query is required"

### 2. No Matches
**Query:** "quantum physics theories"
- **Expected:** Web fallback OR "No information available"

### 3. Very Long Query
**Query:** (300+ characters)
- **Expected:** Still processes, but response limited to 10KB

### 4. Special Characters
**Query:** "crops@#$%^&"
- **Expected:** Handles gracefully, matches "crops"

---

## Performance Benchmarks

- **Local KB Search:** < 50ms
- **Web Fallback:** < 5 seconds (timeout limit)
- **Total Response Size:** < 10KB
- **HTML/CSS/JS:** < 5KB combined

---

## Hackathon Demo Script

1. **Show the Interface**
   - Point out minimal design
   - Show file sizes (CSS < 2KB)

2. **Demo Single Keyword**
   - Query: "irrigation"
   - Show LOCAL source badge
   - Point out matched keywords

3. **Demo Multi-Keyword (The Magic!)**
   - Query: "crops for summer weather"
   - Explain how it found multiple matches
   - Show combined response
   - Highlight scoring system

4. **Demo Web Fallback**
   - Query: "latest news"
   - Show WEB source badge
   - Point out bandwidth usage

5. **Show Response Size**
   - Point out "bytes" counter
   - Explain 10KB limit
   - Show truncation if needed

---

## Troubleshooting Common Issues

**Issue:** "ModuleNotFoundError: No module named 'django'"
- **Fix:** `pip install -r requirements.txt`

**Issue:** No matches for obvious queries
- **Fix:** Add more keywords to knowledge_base/data.txt

**Issue:** Web search timing out
- **Fix:** Check internet connection or increase WEB_SEARCH_TIMEOUT

**Issue:** Port 8000 already in use
- **Fix:** `python manage.py runserver 8080`

---

## Success Criteria

✅ Local KB returns results for agriculture queries  
✅ Multi-keyword queries combine multiple entries  
✅ Relevance scores rank results correctly  
✅ Web fallback works when no local match  
✅ All responses under 10KB  
✅ Interface loads in < 1 second on slow connection  
✅ No errors in console  

---

Good luck with your hackathon! 🚀
