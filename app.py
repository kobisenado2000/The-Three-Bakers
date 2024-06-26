from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import pyodbc as odbc

SERVER = 'DESKTOP-40EQ1M0'
DATABASE = 'WEB'
DRIVER_NAME = 'SQL SERVER'

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={{{SERVER}}};
    DATABASE={{{DATABASE}}};
    Trust_Connection=yes;
"""
conn = odbc.connect(connection_string)
cursor = conn.cursor()
print(conn)


app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        Username = request.form['Username']
        Passwords = request.form['Passwords']
        authenticate, role , UserID = authenticate_user(Username, Passwords) 


        if authenticate==True: 
            session['Username'] = Username 
            session['UserID'] = UserID
            session['role'] = role
            if role == 'customer':
                return redirect(url_for('menu'))
            else: 
                return redirect(url_for('nihul'))
        else:
            return render_template('error.html', error_message="שם משתמש או סיסמא לא נכונים")
    return render_template('login.html')


@app.route('/menu', methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        data = request.get_json()  
        TotalPrice= data.get('TotalPrice')
        UserID = session.get('UserID')

        insert_order_and_items( UserID,  TotalPrice)
        return jsonify({'status': 'success'}), 200
    
    else:
        cursor.execute("SELECT ItemName, Description, Price, image_name FROM MenuItems")
        menu_items = cursor.fetchall()
        return render_template('menu.html', menu_items=menu_items)

@app.route('/nihul', methods=['GET','POST'])
def nihul():
    if 'Username' in session and session['role']!='customer': 
        if session['role']!='customer':
            if request.method == 'POST':
                form_id = request.form.get('form_id')
                if form_id == 'add_menu_item':
                    ItemName=request.form['ItemName']
                    Description=request.form['Description']
                    Price=request.form['Price']
                    image_name=request.form['image_name']
                    add_new_menu_item(ItemName, Description, Price, image_name)
                    return render_template('success.html', success_message=f"הפריט התווסף בהצלחה!")
                elif form_id == 'action-form':
                    OrderID = request.form['OrderID']
                    Status = request.form['Status']
                    close_order(Status, OrderID)
                    return render_template('success.html', success_message=f"ההזמנה נסגרה בהצלחה!")
            else:
                cursor.execute('SELECT * FROM Orders')
                data = cursor.fetchall() 
                cursor.execute('SELECT * FROM Reviews')
                data_Reviews = cursor.fetchall()
                return render_template('nihul.html',data=data , data_Reviews=data_Reviews)
        else:
            return render_template('error.html', error_message=f"אין הרשאות לניהול המערכת")
    else:
        return render_template('error.html', error_message=f"אין הרשאות לניהול המערכת")
        

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Username = request.form['Username']
        Passwords = request.form['Passwords']
        Email = request.form['Email']
        role = request.form['role']  
        if password_exists(Passwords):
            return render_template('error.html', error_message=f"שם משתמש וסיסמא כבר קיימים")
        
        else:
            add_new_user(Username, Passwords, Email, role)
            return render_template('success.html', success_message=f"המשתמש נוסף בהצלחה!") 
        
    return render_template('register.html')

    
@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        Username=request.form['Username']
        Rating=request.form['Rating']
        Comment=request.form['Comment']
        ImageURL=request.form['ImageURL']
        try:
            add_review_to_db(Username, Rating, Comment, ImageURL)
            return render_template('success.html', success_message=f"הביקורת נוספה בהצלחה!") 
        except:
            return render_template('error.html', error_message=f"שגיאה בהוספת הביקורת")
    else:
        return render_template('review.html')
        

from model import *  

if __name__ == '__main__':
    app.run(debug=True)



