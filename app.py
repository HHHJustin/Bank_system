import psycopg2
from flask import *

conn = psycopg2.connect(database="bank-database", 
                        user="postgres", 
                        password="zxcv4567", 
                        host="127.0.0.1", port="5432")

# postgresql : 
# 1. id (real) 
# 2. nickname(varchar[20]) length(nickname) > 6 
# 3. username(varchar[20]) length(username) > 6 
# 4. password(varchar[20]) length(username) > 6 
# 5. balance (int)
cursor = conn.cursor()
# cur.execute("SELECT * FROM users;")
# data = cur.fetchall()
# print(data)

app = Flask(__name__,
            static_folder="public",
            static_url_path= "/"
            )
app.secret_key = "zxcv4567"
# 首頁 1. 登入input username and password (session['username'] = username) 2. 註冊 超連結
@app.route("/")
def index():
    return render_template("index.html")

# 錯誤頁面 錯誤（標題）+ 錯誤訊息（細節）+ 回首頁超連結 or if session["username"] 有東西 回member首頁
# /error?msg=error messeage
@app.route("/error")
def error():
    message = request.args.get("msg", "Click The Link Back To Front Page")
    return render_template("error.html" , message = message)

# 註冊畫面 1. nickname 2. username 3. password
@app.route("/register")
def register():
    return render_template("register.html")
# TODO: use json format as request body.
# TODO: restful api regard everything as resources so use noun. as much as possible.
#  POST /users or /registration
@app.route("/signup" , methods=["POST"])
def signup():
    nickname = request.form["nickname"]
    account = request.form["account"]
    password = request.form["password"]

    cursor.execute("SELECT account FROM users") #TODO: Use unique constrain or unique index. 
    data = cursor.fetchall()
    account_list = []
    for row in data:
        account_list.append(row[0])
    if account in account_list:
        return redirect("\error?msg=TheAccountIsExisted!")
    else: 
    # cur.execute("INSERT INTO users(id, account, password, nickname) VALUES (1, 'yaya650042', 'zxcv4567', 'Yaya');")
        #TODO: use AUTO_INCREMENT id or uuid.
        # https://www.postgresqltutorial.com/postgresql-tutorial/postgresql-uuid/
        length = len(account_list) + 1
        #TODO: password shouldn't be plain text in database. Use bcrypt to store the password
        # https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt
        cursor.execute("INSERT INTO users(id, account, password, nickname) VALUES (%s, %s, %s, %s);", (length, account, password, nickname))
        conn.commit()
        print("Success!!!")
        return redirect("/")
# POST /users/login
@app.route("/signin", methods=["POST"])
def signin():
    account = request.form["account"]
    password = request.form["password"]
    # Do not select *. Specify the column name. SELECT id, acount, password FROM users;
    # https://tanelpoder.com/posts/reasons-why-select-star-is-bad-for-sql-performance/?source=post_page-----49e769dc3cdc--------------------------------
    cursor.execute("SELECT * FROM users WHERE account = %s AND password = %s;", (account, password))
    user = cursor.fetchone()
    
    if user:
        # TODO: For session base authentication. It should be a nnpredictable secure Random id and reveal no information.
        # https://vicxu.medium.com/authentication-%E9%82%A3%E4%BA%9B%E5%B0%8F%E4%BA%8B%E4%B8%8A%E9%9B%86-cookie-%E8%88%87-session-%E4%BB%8B%E7%B4%B9-1da2d413afa2
        # The session base authentication should fullfil the same origin policy so we can't not separate the FE and BE. 

        # TODO: In the morden web architecture. Token-based authentication is more prefer. The FE and BE can be separated.
        # https://vicxu.medium.com/%E6%B7%BA%E8%AB%87-authentication-%E4%B8%AD%E9%9B%86-token-based-authentication-90139fbcb897
        session["account"] = account

        return render_template("member.html")
    else:
        return redirect("/error?msg=WrongAccountPassWord")


# member 首頁  1. deposit 2. withdraw 3. check the balance 4. logout (del session['username'])
    # deposit form (1. input (number) 2. buttom) -> user['balance'] += xxxxx
    # withdraw form (1. input (number) 2. buttom) -> check if user['balance'] - value < 0 -> yes -> redirect(error page) -> no -> user['balance'] -= value
    # check the balance -> return user['balance']
@app.route("/member", methods=["POST","GET"])
def member():
    if "account" in session:
        return render_template("member.html")
    else: 
        return redirect("/") 

# postgresql : 1. id 2. nickname 3. username 4. password 5. balance

@app.route("/deposit", methods=["POST"])
def deposit():
    deposit_money = request.form["deposit"]
    #TODO: Create a middleware to handle user login.
    # https://fastapi.tiangolo.com/tutorial/middleware/
    # Middleware is a decorator pattern:
    # https://refactoring.guru/design-patterns/decorator
    account = session["account"]
    cursor.execute("SELECT * FROM users WHERE account = %s;", (account,))
    user = cursor.fetchone()
    balance = int(user[4]) + int(deposit_money)
    cursor.execute("UPDATE users SET balance=%s WHERE account=%s;", (balance, account))
    conn.commit()
    return render_template("balance.html", balance=balance)

@app.route("/withdraw", methods=["POST"])
def withdraw():
    deposit_money = request.form["withdraw"]
    account = session["account"]
    cursor.execute("SELECT * FROM users WHERE account = %s;", (account,))
    user = cursor.fetchone()
    if int(user[4]) - int(deposit_money) < 0:
        return render_template("no_money.html")
    else:
        balance = int(user[4]) - int(deposit_money)
        cursor.execute("UPDATE users SET balance=%s WHERE account=%s;", (balance, account))
        conn.commit()
        return render_template("balance.html", balance=balance)

@app.route("/check", methods=["POST"])
def check():
    account = session["account"]
    cursor.execute("SELECT * FROM users WHERE account =%s;",(account,))
    balance = cursor.fetchone()[4]
    return render_template("balance.html", balance=balance)

# cur.close()
@app.route("/logout")
def logout():
    del session["account"]
    return redirect("/")

app.run(port = 3000)
cursor.close()
conn.close()
