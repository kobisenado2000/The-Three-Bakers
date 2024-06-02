import pyodbc as odbc
from app import conn
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header


cursor = conn.cursor()

def authenticate_user(Username, Passwords): #כניסה לאתר - פוקנציה לבדיקה עם המשתמש כבר קיים
    query = "SELECT UserID, Username, Passwords, Role FROM Users WHERE Username = ? AND Passwords = ?"
    try:
        cursor.execute(query, (Username, Passwords))
        user = cursor.fetchone()
        if user and user.Passwords == Passwords:
            role = user[3]  # שמירת התפקיד (Role) מהשורה שנמצאה
            print(role)
            UserID = user[0]
            return True, role , UserID # החזרת התפקיד (Role) מהשורה שנמצאה
        else:
            return False, None, None
    except odbc.Error as e:
        print(f"שגיאה באימות המשתמש: {e}")
        return False, None, None
    
    
def password_exists(Passwords, cursor): #פונקציה לבדיקת שהסיסמא לא קיימת בעת הרשמה
    query = "SELECT COUNT(*) FROM Users WHERE Passwords = ?"

    try:
        cursor.execute(query, (Passwords,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    except odbc.Error as e:
        print(f"שגיאה בבדיקת הסיסמה: {e}")
        return False

        
def add_new_user(Username, Passwords, Email, role): #פונקציה להוספת משתמש
    query = "INSERT INTO Users (Username, Passwords, Email, Role) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(query, (Username, Passwords, Email, role))
        conn.commit()
        print(f"המשתמש {Username} התווסף בהצלחה!")
    except odbc.Error as e:
        print(f"שגיאה בהוספת המשתמש: {e}")


def insert_order_and_items( UserID, TotalPrice ):
    try:
        cursor.execute("INSERT INTO Orders (UserID, Status, TotalPrice) VALUES ( ?, ?, ?)", (UserID, 'Preparing', TotalPrice))
    except odbc.Error as e:
        print(f"שגיאה בהוספת הזמנה: {e}")

    conn.commit()  # Commit the transaction

    
def add_review_to_db(Username, Rating, Comment, ImageURL): #הוספת חוות דעת
    try:
        ReviewDate = datetime.now()
        # ביצוע השאילתה להוספת ביקורת חדשה
        cursor.execute("""
            INSERT INTO Reviews (Username, Rating, Comment, ReviewDate, ImageURL)
            VALUES (?, ?, ?, ?, ?)
        """, (Username, Rating, Comment, ReviewDate, ImageURL))

        conn.commit()
        print("Review added successfully")
        
    except odbc.Error as e:
        print(f"Failed to add review: {e}")
     

def add_new_menu_item(ItemName, Description, Price, image_name): #הוספה פריט לתפריט
    query = """
    INSERT INTO MenuItems (ItemName, Description, Price, IsAvailable,image_name) 
    VALUES (?, ?, ?, ?,?)
    """
    try:
        cursor.execute(query, (ItemName, Description, Price, 1, image_name))
        conn.commit()
        print(f"הפריט {ItemName} התווסף בהצלחה לתפריט!")
    except odbc.Error as e:
        print(f"שגיאה בהוספת הפריט לתפריט: {e}")


def close_order(Status, OrderID): #סגירת הזמנה
    cursor.execute("UPDATE Orders SET Status =? WHERE OrderID = ?", (Status, OrderID,))
    conn.commit()
    if Status == 'Completed':
        cursor.execute("SELECT * FROM Orders WHERE OrderID = ?", (OrderID,))
        order = cursor.fetchone()
        cursor.execute("SELECT * FROM Users WHERE UserID = ?", (order.UserID,))
        user = cursor.fetchone()
        subject = Header('מאפיית שלושת האופים', 'utf-8')
        body = 'הזמנה שלך מוכנה, נשמח לראותך בקרוב בחנות שלנו'
        send_email(user.Email,subject,body)
        
def send_email(Email,subject,body): #שליחת מייל
    smtp_server = "smtp.gmail.com"  # שרת SMTP של גוגל
    smtp_port = 587  # פורט סטנדרטי עם אבטחה
    sender_email = "nivbms@gmail.com" 
    receiver_email = (Email)
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        # יצירת חיבור לשרת SMTP
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()  # יצירת חיבור מאובטח
        smtp.login(sender_email, "gupi rblo wuxc yetf")  # <-- שנה כאן את הסיסמה שלך

        # שליחת המייל
        smtp.sendmail(sender_email, receiver_email, msg.as_string())
        print("המייל נשלח בהצלחה!")

    except Exception as e:
        print(f"שגיאה בשליחת המייל: {e}")

    finally:
        smtp.quit()  # ניתוק מהשרת
        