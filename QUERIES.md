# 📝 Example Queries for Geo-SQL Agent

Test these queries to see the AI in action!

## 🟢 Basic Queries (Simple)

### 1. List all cafes
```
Show me all cafes
```

**Expected SQL:**
```sql
SELECT id, name, address, ST_AsGeoJSON(geom) as geojson
FROM cafes;
```

### 2. List all parks
```
Show all parks
```

**Expected SQL:**
```sql
SELECT id, name, area, ST_AsGeoJSON(geom) as geojson
FROM parks;
```

### 3. Large parks only
```
Show all parks larger than 5000 square meters
```

**Expected SQL:**
```sql
SELECT id, name, area, ST_AsGeoJSON(geom) as geojson
FROM parks
WHERE area > 5000;
```

---

## 🟡 Intermediate Queries (Spatial Operations)

### 4. Cafes near largest park
```
Find all cafes within 200 meters of the largest park
```

**Expected SQL:**
```sql
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c, parks p
WHERE p.area = (SELECT MAX(area) FROM parks)
AND ST_DWithin(c.geom::geography, p.geom::geography, 200);
```

### 5. Cafes near roads
```
Find cafes within 50 meters of main roads
```

**Expected SQL:**
```sql
SELECT DISTINCT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c, roads r
WHERE r.road_type = 'main'
AND ST_DWithin(c.geom::geography, r.geom::geography, 50);
```

### 6. Closest cafe to smallest park
```
What is the closest cafe to the smallest park?
```

**Expected SQL:**
```sql
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson,
       ST_Distance(c.geom::geography, p.geom::geography) as distance
FROM cafes c, parks p
WHERE p.area = (SELECT MIN(area) FROM parks)
ORDER BY ST_Distance(c.geom::geography, p.geom::geography)
LIMIT 1;
```

---

## 🔴 Advanced Queries (Complex Spatial Joins)

### 7. Roads intersecting parks
```
Show all roads that intersect with parks
```

**Expected SQL:**
```sql
SELECT DISTINCT r.id, r.name, r.road_type, ST_AsGeoJSON(r.geom) as geojson
FROM roads r, parks p
WHERE ST_Intersects(r.geom, p.geom);
```

### 8. Parks near Rothschild Boulevard
```
Find parks within 100 meters of Rothschild Boulevard
```

**Expected SQL:**
```sql
SELECT p.id, p.name, p.area, ST_AsGeoJSON(p.geom) as geojson
FROM parks p, roads r
WHERE r.name LIKE '%Rothschild%'
AND ST_DWithin(p.geom::geography, r.geom::geography, 100);
```

### 9. Cafe density analysis
```
Count how many cafes are within 500m of each park
```

**Expected SQL:**
```sql
SELECT p.id, p.name, COUNT(c.id) as cafe_count,
       ST_AsGeoJSON(p.geom) as geojson
FROM parks p
LEFT JOIN cafes c ON ST_DWithin(p.geom::geography, c.geom::geography, 500)
GROUP BY p.id, p.name, p.geom;
```

### 10. Multi-step buffer query
```
Find all cafes in a 300m buffer around parks larger than 10000 sq meters
```

**Expected SQL:**
```sql
SELECT c.id, c.name, ST_AsGeoJSON(c.geom) as geojson
FROM cafes c
WHERE EXISTS (
    SELECT 1
    FROM parks p
    WHERE p.area > 10000
    AND ST_DWithin(c.geom::geography, p.geom::geography, 300)
);
```

---

## 🌍 Multilingual Queries (Hebrew)

### 11. Hebrew query 1
```
מצא את כל בתי הקפה במרחק 200 מטר מהפארק הכי גדול
```

**Translation:** "Find all cafes within 200 meters of the largest park"

### 12. Hebrew query 2
```
הצג את כל הפארקים הגדולים מ-5000 מטר רבוע
```

**Translation:** "Show all parks larger than 5000 square meters"

---

## 🎯 Creative/Tricky Queries

### 13. Named location
```
Find cafes near Dizengoff Street
```

### 14. Comparative query
```
Which park has the most cafes within 300 meters?
```

### 15. Negation query
```
Show me parks that have no roads intersecting them
```

### 16. Distance ranking
```
List all cafes sorted by distance from Independence Park
```

### 17. Complex filter
```
Find cafes that are within 100m of a park but NOT within 50m of a road
```

---

## 🧪 Edge Cases (Testing AI Robustness)

### 18. Ambiguous query
```
Find stuff near things
```
*Should ask for clarification or make best guess*

### 19. Impossible query
```
Find cafes on Mars
```
*Should return empty results or error gracefully*

### 20. Typos
```
Shwo me cafes neer the bigest prk
```
*Should still understand intent*

---

## 🎓 Educational Queries (Learning PostGIS)

### 21. Area calculation
```
What is the total area of all parks combined?
```

### 22. Average distance
```
What's the average distance between cafes and the nearest park?
```

### 23. Geometric center
```
Find the geographic center of all cafes
```

---

## 🏆 Demo Sequence for Video

**Use this sequence for a compelling demo:**

1. **Start Simple:**
   - "Show me all cafes" *(proves it works)*

2. **Add Complexity:**
   - "Find cafes within 200m of the largest park" *(shows spatial intelligence)*

3. **Show Map Integration:**
   - Watch results appear on map in real-time

4. **Multilingual:**
   - Ask in Hebrew *(shows language flexibility)*

5. **Complex Analysis:**
   - "Which park has the most cafes nearby?" *(shows analytical power)*

6. **Explain the Magic:**
   - Show the generated SQL in the console
   - Point out the system prompt in code

---

## 📊 Benchmarking Results

| Query Type | Expected Time | Results |
|------------|---------------|---------|
| Simple list | < 100ms | 15 cafes |
| Distance query | < 200ms | 3-5 cafes |
| Complex join | < 300ms | Variable |
| Aggregation | < 400ms | Summary |

---

## 💡 Tips for Best Results

1. **Be specific:** "200 meters" is better than "nearby"
2. **Use table names:** "cafes" and "parks" are recognized
3. **Mention measurements:** "square meters", "meters", etc.
4. **Ask follow-ups:** The AI remembers context

---

## 🐛 Known Limitations

- Only works with predefined tables (cafes, parks, roads)
- Distance is always in meters (due to geography cast)
- Some very complex nested queries might fail
- Requires valid OpenAI API key

---

## 🔮 Future Query Ideas

Ideas for extending the system:

- "Draw a 500m buffer around all parks"
- "Find the shortest path between two cafes"
- "Show me a heatmap of cafe density"
- "Calculate the convex hull of all parks"
- "Find clusters of cafes using DBSCAN"

---

**Ready to test?** Start with query #1 and work your way up!

**Pro tip:** Watch the generated SQL to learn PostGIS syntax! 📚
