# 🎯 START HERE - למתחילים

> **רק רוצה להריץ? תעקוב אחרי 4 השלבים האלה**

---

## ✅ שלב 1: בדוק שיש לך Docker

### Windows/Mac:
1. לך ל-https://www.docker.com/products/docker-desktop/
2. הורד ו תתקין
3. פתח את Docker Desktop
4. וודא שאתה רואה לוגו ירוק (רץ)

### בדיקה:
פתח טרמינל והקלד:
```bash
docker --version
```

אם אתה רואה: `Docker version 28.x.x` → **מעולה! ✅**

---

## ✅ שלב 2: קבל OpenAI API Key

1. לך ל-https://platform.openai.com/api-keys
2. לחץ על **"Create new secret key"**
3. העתק את המפתח (מתחיל ב-`sk-...`)
4. שמור אותו - תצטרך בשלב הבא

**💰 כמה זה עולה?** כ-$0.01 לשאלה (סנט אחד)

---

## ✅ שלב 3: הרץ את המערכת

פתח טרמינל בתיקיית הפרויקט והרץ:

### Windows:
```bash
echo OPENAI_API_KEY=sk-paste-your-key-here > .env
docker-compose up -d
```

### Mac/Linux:
```bash
echo "OPENAI_API_KEY=sk-paste-your-key-here" > .env
docker-compose up -d
```

**תחליף** `sk-paste-your-key-here` במפתח שקיבלת בשלב 2!

תראה משהו כזה:
```
✔ Container geo-sql-postgis   Started
✔ Container geo-sql-backend   Started
✔ Container geo-sql-frontend  Started
```

**אם רואה 3 ✔ → זה עובד! ✅**

---

## ✅ שלב 4: פתח בדפדפן

לך ל:
```
http://localhost:3010
```

אמור לראות:
- 🗺️ **מפה** של תל אביב
- 📝 **תיבת טקסט** לשאלות
- 🔘 **כפתור Execute**

---

## 🎯 עכשיו תנסה!

הקלד בתיבה:
```
Show me all cafes
```

לחץ **Execute**

**אמור לקרות:**
1. ⏳ ספינר טעינה (2-3 שניות)
2. 📄 SQL מופיע בקונסול
3. 📍 נקודות כחולות מופיעות על המפה
4. 📊 "Results: 15 cafes"

**אם זה קרה → מזל טוב! המערכת עובדת! 🎉**

---

## 💬 מה עוד אפשר לשאול?

נסה את אלה:

### בעברית:
```
הצג את כל בתי הקפה
```

```
מצא פארקים גדולים מ-5000 מטר רבוע
```

```
איזה פארק יש הכי הרבה בתי קפה בקרבתו
```

### באנגלית:
```
Find cafes within 200 meters of the largest park
```

```
What is the closest cafe to the smallest park?
```

```
Show roads that intersect with parks
```

---

## 🐛 משהו לא עובד?

### ❌ "Port already allocated"
**תקן:**
1. פתח את הקובץ `docker-compose.yml`
2. מצא `5432:5432`
3. שנה ל-`5433:5432`
4. הרץ שוב: `docker-compose up -d`

### ❌ "OpenAI API key not found"
**תקן:**
1. וודא שיצרת קובץ `.env`
2. וודא שהמפתח נכון (מתחיל ב-`sk-`)
3. הרץ: `docker-compose restart backend`

### ❌ "Connection refused"
**תקן:**
1. וודא ש-Docker Desktop רץ (לוגו ירוק)
2. וודא שכל הקונטיינרים פועלים: `docker-compose ps`
3. אם לא - הפעל מחדש: `docker-compose down && docker-compose up -d`

### ❌ המפה לא טוענת
**תקן:**
1. רענן את הדפדפן: **Ctrl + Shift + R**
2. פתח Console (F12) וחפש שגיאות אדומות

---

## 🆘 עדיין תקוע?

### 1. בדוק לוגים:
```bash
docker-compose logs -f backend
```

תראה מה השרת אומר

### 2. בדוק שהשרת רץ:
```bash
curl http://localhost:8000/health
```

אמור לקבל: `{"status":"healthy","database":"connected"}`

### 3. התחל מההתחלה:
```bash
docker-compose down
docker-compose up -d
```

---

## 📚 רוצה להבין יותר?

אחרי שהמערכת רצה, קרא:

| מה אתה רוצה | קרא את |
|-------------|---------|
| **הבנה בסיסית (5 דק')** | [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md) |
| **מדריך מלא בעברית** | [USAGE_GUIDE.md](USAGE_GUIDE.md) |
| **איך זה עובד** | [WORKFLOW.md](WORKFLOW.md) |
| **פקודות מהירות** | [CHEAT_SHEET.md](CHEAT_SHEET.md) |
| **ארכיטקטורה טכנית** | [ARCHITECTURE.md](ARCHITECTURE.md) |

---

## 🎬 סיכום מהיר

### התקנה (פעם אחת):
```bash
# 1. הורד Docker Desktop
# 2. קבל OpenAI API Key
# 3. הרץ:
echo "OPENAI_API_KEY=sk-your-key" > .env
docker-compose up -d
```

### שימוש יומיומי:
```bash
# התחל:
docker-compose up -d

# עבוד:
# פתח http://localhost:3010
# שאל שאלות

# סיים:
docker-compose down
```

---

## ✨ זהו!

**עכשיו אתה מוכן להתחיל לשאול שאלות בשפה טבעית ולקבל SQL queries + מפות!**

**שאלה ראשונה מומלצת:**
```
Show me all cafes
```

**בהצלחה! 🚀**

---

**יש בעיה?** פתח issue: https://github.com/moshe084/MasterRepo/issues
