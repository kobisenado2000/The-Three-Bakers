The-Three-Bakers
הפרויקט הוא אתר אינטרנט לבית מאפה המאפשר ללקוחות להזמין מגוון מוצרי מאפה מתפריט מקוון, ולצפות בחוות דעת של לקוחות אחרים. בנוסף, האתר מאפשר למנהלי המאפייה לנהל את ההזמנות, לסגור אותן כשהן מוכנות, ולעדכן את התפריט עם מוצרים חדשים. המערכת מבוססת על מודל MVC כדי להפריד בין הלוגיקה העסקית, התצוגה והבקרה.

סוגי משתמשים:
1. לקוח - יכול להיכנס לאתר, לגלוש בתפריט המוצרים, להוסיף מוצרים לסל הקניות, להזמין ולשלם עבור ההזמנה שלו. הלקוח יכול גם לכתוב חוות דעת על המאפייה ולצרף תמונה.
2. מנהל - יכול לצפות ברשימת ההזמנות הפתוחות, לסמן הזמנות כ"הושלמו" ולשלוח מייל ללקוח על כך. המנהל יכול גם להוסיף פריטים חדשים לתפריט המוצרים, לערוך פרטים של מוצרים קיימים ולצפות בחוות הדעת של הלקוחות.
3. עובד - יכול לצפות ברשימת ההזמנות הפתוחות, לסגור אותם ולבצע פעולות נוספות.

תהליכים עיקריים:
1. הזמנת מוצרים:
   - הלקוח גולש בתפריט המקוון ובוחר את המוצרים שהוא רוצה להזמין.
   - הלקוח מוסיף את המוצרים לסל הקניות ומזין את פרטי המשלוח והתשלום.
   - נתוני ההזמנה נשמרים בטבלת "Orders" בבסיס הנתונים.
   - מייל אישור נשלח ללקוח לאחר ההזמנה המוצלחת.
2. סגירת הזמנה:
   - המנהל יכול לצפות ברשימת ההזמנות הפתוחות בלוח הבקרה שלו.
   - לאחר הכנת ההזמנה, המנהל יכול לסמן אותה כ"הושלמה".
   - מייל נשלח ללקוח עם הודעה שההזמנה שלו מוכנה לאיסוף.
3. ניהול תפריט:
   - המנהל יכול להוסיף פריטים חדשים לתפריט המוצרים על ידי מילוי פרטי המוצר (שם, תיאור, מחיר ותמונה).
   - המנהל יכול גם לערוך או להסיר מוצרים קיימים מהתפריט.
4. חוות דעת:
   - הלקוח יכול לכתוב חוות דעת על המאפייה, לדרג אותה בסולם של 1-5 כוכבים וגם לצרף תמונה.
   - חוות הדעת נשמרות בטבלת "Reviews" בבסיס הנתונים.
   - המנהל יכול לצפות בחוות הדעת של הלקוחות בלוח הבקרה שלו.

נתונים מנוהלים:
1. משתמשים (Users) - מכיל פרטי המשתמשים (שם משתמש, סיסמה, אימייל, תפקיד).
2. הזמנות (Orders) - מכיל פרטי ההזמנות (מזהה הזמנה, מזהה משתמש, סטטוס, סכום כולל).
3. פריטי תפריט (MenuItems) - מכיל את רשימת המוצרים בתפריט (שם, תיאור, מחיר, תמונה, זמינות).
4. חוות דעת (Reviews) - מכיל את חוות הדעת של הלקוחות (שם משתמש, דירוג, תוכן הביקורת, תאריך, תמונה).

ארכיטקטורה כוללת:
האתר מבוסס על מודל MVC כדלקמן:

1. Model (model.py): מכיל את כל הלוגיקה העסקית של האפליקציה, כולל:
   - פונקציות לאימות משתמשים, הוספת משתמשים חדשים ובדיקת קיום סיסמאות.
   - פונקציות להוספת הזמנות חדשות, הוספת חוות דעת וסגירת הזמנות.
   - פונקציה להוספת פריטים חדשים לתפריט.
   - פונקציית עזר לשליחת מיילים.
   - האינטראקציה עם בסיס הנתונים מתבצעת באמצעות ספריית pyodbc.
2. View (templates/): מכיל את קבצי ה-HTML עבור התצוגות השונות:
   - home.html - דף הבית
   - login.html - דף התחברות
   - register.html - דף הרשמה
   - menu.html - דף התפריט המקוון
   - nihul.html - לוח הבקרה של המנהל
   - review.html - טופס להוספת חוות דעת
   - error.html - דף שגיאה
   - success.html - דף הצלחה
3. Controller (app.py): מקשר בין ה-Model ל-View, מעבד בקשות משתמש ומנתב אותן ליעדים המתאימים:
   - ניתוב הבקשות באמצעות דקורטורים של Flask.
   - בקרה על תהליכי הזמנה, התחברות, הרשמה, ניהול תפריט וחוות דעת.
   - שימוש בסשן להחזקת מצב המשתמש.
   - שליחת נתונים מהמודל לתצוגה ולהיפך.

התקנים נדרשים:
- Python 3.x
- Flask
- pyodbc
- SQL Server

**Login:**
![image](![תמונה של WhatsApp‏ 2024-06-02 בשעה 18 35 58_090d7dd2](https://github.com/kobisenado2000/The-Three-Bakers/assets/169029225/213d2955-3491-4b15-a41f-55b2cea0e82c)
)
**Menu:**
![image](![תמונה של WhatsApp‏ 2024-06-02 בשעה 18 38 26_d6ab0b76](https://github.com/kobisenado2000/The-Three-Bakers/assets/169029225/149f2a87-1725-433b-8c05-981bdf639436)
)
**Manager Page:**
![image](![תמונה של WhatsApp‏ 2024-06-02 בשעה 18 38 42_f5c44582](https://github.com/kobisenado2000/The-Three-Bakers/assets/169029225/33bf04a6-b24b-44f6-8012-36aa2b0e7f78)
)
**Review:**
![image](![תמונה של WhatsApp‏ 2024-06-02 בשעה 18 38 56_27edba73](https://github.com/kobisenado2000/The-Three-Bakers/assets/169029225/ef4da9f2-16a4-4e29-8104-2047cfceaae6)
)
**Auto Email:**
![image](https://github.com/kobisenado2000/The-Three-Bakers/assets/170872792/ae488afe-4021-4b00-9150-ba1c5392fe51)



