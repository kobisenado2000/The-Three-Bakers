from app import conn
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

cursor = conn.cursor()

def authenticate_user(Username, Passwords): 
    query = "SELECT UserID, Username, Passwords, Role FROM Users WHERE Username = ? AND Passwords = ?"
    try:
        cursor.execute(query, (Username, Passwords))
        user = cursor.fetchone()
        if user and user.Passwords == Passwords:
            role = user[3]  
            UserID = user[0]
            return True, role , UserID 
        else:
            return False, None, None
    except:
        return False, None, None
    
    
def password_exists(Passwords): 
    query = "SELECT COUNT(*) FROM Users WHERE Passwords = ?"

    try:
        cursor.execute(query, (Passwords,))
        count = cursor.fetchone()[0]
        if count > 0:
            return True
        else:
            return False
    except:
        return False

        
def add_new_user(Username, Passwords, Email, role): 
    query = "INSERT INTO Users (Username, Passwords, Email, Role) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(query, (Username, Passwords, Email, role))
        conn.commit()
    except:
        return False


def insert_order_and_items( UserID, TotalPrice ):
    try:
        cursor.execute("INSERT INTO Orders (UserID, Status, TotalPrice) VALUES ( ?, ?, ?)", (UserID, 'Preparing', TotalPrice))
    except:
        return False

    conn.commit()  

    
def add_review_to_db(Username, Rating, Comment, ImageURL): 
    try:
        ReviewDate = datetime.now()
        cursor.execute("""
            INSERT INTO Reviews (Username, Rating, Comment, ReviewDate, ImageURL)
            VALUES (?, ?, ?, ?, ?)
        """, (Username, Rating, Comment, ReviewDate, ImageURL))

        conn.commit()
        
    except:
        return False
     

def add_new_menu_item(ItemName, Description, Price, image_name): 
    query = """
    INSERT INTO MenuItems (ItemName, Description, Price, IsAvailable,image_name) 
    VALUES (?, ?, ?, ?,?)
    """
    try:
        cursor.execute(query, (ItemName, Description, Price, 1, image_name))
        conn.commit()
    except :
        return False


def close_order(Status, OrderID): 
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
        
def send_email(Email,subject,body): 
    smtp_server = "smtp.gmail.com"  
    smtp_port = 587  
    sender_email = "nivbms@gmail.com" 
    receiver_email = (Email)
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        smtp = smtplib.SMTP(smtp_server, smtp_port)
        smtp.starttls()  
        smtp.login(sender_email, "gupi rblo wuxc yetf")  

        smtp.sendmail(sender_email, receiver_email, msg.as_string())

    except:
        return False

    finally:
        smtp.quit()  
        