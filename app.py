# coding:utf-8

from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route("/")
def index():
    return "Hello, World!foooo"


@app.route("/user/<username>")
def show_user_profile(username):
    return "User {}".format(username)

@app.route("/user<username>")
def show_user_profile2(username):
    return "ユーザ {}".format(username)

@app.route("/post/<int:post_id>")
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return "Post {}".format(post_id)

@app.route("/path/<path:subpath>")
def show_subpath(subpath):
    # show the subpath after /path/
    return "Subpath {}".format(subpath)

@app.route('/users')
def show_users():
    users = ["太郎", "花子", "一浪"]
    return render_template('users.html', users=users)

@app.route("/send")
def send():
    return render_template('send.html')

from flask import request
@app.route("/receive", methods=["GET"])
def receive():
    print(request.args.keys)
    if "my_name" in request.args.keys() and request.args["my_name"] != "":
        return "ここに入力した名前を表示： {}".format(request.args["my_name"])
    else:
        return "名前が未入力です"


@app.route("/get_sample")
def get_sample():
    return render_template('get_sample.html', query=request.args.get("query", "d2c"))

@app.route("/post_sample", methods=["GET"])
def sample(gender=""):
    return render_template('post_sample.html', gender=gender)

@app.route("/post_sample", methods=["POST"])
def post_sample():
    gender = request.form.get("gender","")
    return sample(gender)



@app.route("/post_work", methods=["GET"])
def sample1(name="", gender="", mail=""):
    return render_template('post_work1.html', name=name, gender=gender, mail=mail)

@app.route("/post_work", methods=["POST"])
def post_sample1():
    name = request.form.get("my_name","")
    gender = request.form.get("gender","")
    mail = request.form.get("mail","")
    return sample1(name, gender, mail)

@app.route("/post_send")
def post_send():
    return render_template('post_send.html')

# @app.route("/post_receive", methods=["POST"])
# def post_receive():
#     if request.form.get("my_name", "") != ""  :
#         return "ようこそ {}".format(request.form["my_name"])
#     else:
#         return "名前を入力してください"

@app.route("/post_receive", methods=["POST"])
def post_receive():
    if request.form.get("my_name", "") != ""  :
        user_name = request.form["my_name"]
        return render_template("post_receive.html", user_name=user_name)
    else:
        post_error_message = "名前を入力してください"
        return render_template("post_receive.html", post_error_message=post_error_message)

import random

@app.route("/post_janken", methods=["GET"])
def jankenpon(user_choice="", com_choice="", judge=""):
    return render_template('post_janken.html', user_choice=user_choice, com_choice=com_choice, judge=judge)

@app.route("/post_janken", methods=["POST"])
def post_janken():
    user_choice = request.form.get("janken", "")

    jankenList = ["グー", "チョキ", "パー"]
    com_choice = random.choice(jankenList)

    draw = "引き分け"
    win = "勝ち！"
    lose = "負け！"

    if user_choice == com_choice:
        judge = draw
    else:
        if user_choice == "グー":
            if com_choice == "チョキ":
                judge = win
            else:
                judge = lose

        elif user_choice == "チョキ":
            if com_choice == "パー":
                judge = win
            else:
                judge = lose

        else:
            if com_choice == "グー":
                judge = win
            else:
                judge = lose

    return jankenpon(user_choice, com_choice, judge)


import mysql.connector
from mysql.connector import errorcode

@app.route("/mysql_select")
def mysql_select():
    host = 'localhost'
    username = 'root' 
    passwd = 'wako19980207'
    dbname = 'my_database'

    goods = []
    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        query = 'SELECT goods_id, goods_name, price FROM goods_table'
        cursor.execute(query)

        for (id, name, price) in cursor:
            item = {"goods_id":id, "goods_name":name, "price":price}
            goods.append(item)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()
    return render_template("goods.html", goods = goods)


@app.route("/mysql_sample")
def mysql_sample():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'wako19980207'    # MySQLのパスワード
    dbname   = 'my_database'    # データベース名

    order = ""
    if "order" in request.args.keys() :
            print(request.args)
            order = request.args.get("order")

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        
        query = 'SELECT goods_name, price FROM goods_table ORDER BY price ' + order
        cursor.execute(query)
        goods = []
        for (name, price) in cursor:
            item = {"name": name, "price":price}
            goods.append(item)
        params = {
        "asc_check" : order == "ASC",
        "desc_check" : order == "DESC",
        "goods" : goods
        }
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template("goods.html", **params)


@app.route("/mysql_change")
def mysql_change():
    # import部分は省略
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'wako19980207'    # MySQLのパスワード
    dbname   = 'my_database'    # データベース名

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        query = 'UPDATE goods_table SET price = 60 WHERE goods_id = 5'
        cursor.execute(query)
        cnx.commit() # この処理が無いと変更が反映されません！

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return "終了"


@app.route("/mysql_job")
def challenge_mysql_select():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'wako19980207'    # MySQLのパスワード
    dbname   = 'my_database'    # データベース名


    order = ""
    if "order" in request.args.keys() :
            print(request.args)
            order = request.args.get("order")

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        if order == "":
            query = "select * from emp_table"
        else:
            query = f"select * from emp_table where job = {order}"

        
        # query = "SELECT * FROM emp_table " + b
        # query = f"SELECT * FROM emp_table WHERE job = '{order}'"
        cursor.execute(query)
        goods = []
        for (id, name, job, age) in cursor:
            item = {"id": id, "name": name, "job":job, "age":age}
            goods.append(item)
        params = {
        # "all_check" : order == "",
        # "manager_check" : order == "manager",
        # "analyst_check" : order == "analyst",
        # "clerk_check" : order == "clerk",
        "goods" : goods
        }
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template("mysql_job.html", **params)