import smtplib
from email.mime.text import MIMEText
from email.header import Header

# פרטי השרת וכתובות המייל
smtp_server = "smtp.gmail.com"  # שרת SMTP של גוגל
smtp_port = 587  # פורט סטנדרטי עם אבטחה
sender_email = "nivbms@gmail.com"  # <-- שנה כאן את כתובת המייל שלך
receiver_email = "omerganon@gmail.com"  # <-- שנה כאן את כתובת המייל של הנמען

subject = Header('מאפיית שלושת האופים', 'utf-8')
body = ' הזמנה שלך התקבלה בהצלחה! נשמח לראותך בקרוב בחנות שלנו'
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