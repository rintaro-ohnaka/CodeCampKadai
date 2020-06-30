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


# 12章課題1 emp_tableのデータを表示するプログラム
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
            query = f"select * from emp_table where job = '{order}' "

        
        # query = "SELECT * FROM emp_table " + b
        # query = f"SELECT * FROM emp_table WHERE job = '{order}'"
        cursor.execute(query)
        emps = []
        for (id, name, job, age) in cursor:
            item = {"id": id, "name": name, "job":job, "age":age}
            emps.append(item)
        params = {
        # "all_check" : order == "",
        # "manager_check" : order == "manager",
        # "analyst_check" : order == "analyst",
        # "clerk_check" : order == "clerk",
        "emps" : emps
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




# 12章の課題2　goods_tableに新しい商品データの追加が行えるプログラム
# @app.route("/mysql_insert")
# def challenge_mysql_insert():
#     host = 'localhost'
#     username = 'root'
#     passwd = 'wako19980207'
#     dbname = 'my_database'

#     message = ""
#     order = ""
#     price_order = ""
#     # if "order" in request.args.keys() :
#     #         order = request.args.get("order")
#     # elif "price_order" in request.args.keys() :
#     #         price_order = request.args.get("price_order")

#     if "order" in request.args.keys() and "price_order" in request.args.keys() :
#             order = request.args.get("order")
#             price_order = request.args.get("price_order")

#     try:
#         cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
#         cursor = cnx.cursor()

#         # if order == "" and price_order == "":
#         #     query = "select goods_name, price from goods_table"
#         #     cursor.execute(query)
#         # else:
#         #     query = f"INSERT INTO goods_table (goods_name, price) values ('{order}', '{price_order}') " 
#         #     cursor.execute(query)
#         #     cnx.commit()

#         #     # if int == type(price_order):
#         #     #     message = ['追加成功']
#         #     # else:
#         #     #     message = ['追加失敗']

#         #     # ここに追加成功か、追加失敗かの条件分岐を書く？
#         #     query2 = "select goods_name, price from goods_table"  
#         #     cursor.execute(query2)



#         if order == "" and price_order == "":
#             query = "select goods_name, price from goods_table"
#             cursor.execute(query)
#             print("値が入ってないので実行できない")
#             message = '実行できません'

#         elif order.isdecimal() != True and price_order.isdecimal() == True:
#             query = f"INSERT INTO goods_table (goods_name, price) values ('{order}', {price_order}) " 
#             cursor.execute(query)
#             cnx.commit()
#             query2 = "select goods_name, price from goods_table"  
#             cursor.execute(query2)
#             print("商品が追加できた")
#             message = '追加成功'

#         else:
#             query2 = "select goods_name, price from goods_table"
#             cursor.execute(query2)
#             print("商品追加に失敗")
#             message = '追加失敗'

#         # cursor.execute(query)
#         # cursor.execute(query2)

#         # goods = []
#         # for (name, price) in cursor:
#         #     item = {"name":name, "price":price}
#         #     goods.append(item)

        
#         goods = []
#         for (name, price) in cursor:
#             item = {"name":name, "price":price}
#             goods.append(item)

#         params = {
#         "goods" : goods,
#         "message" : message
#         # "message" : message
#         }

#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#             print("ユーザ名かパスワードに問題があります。")
#         elif err.errno == errorcode.ER_BAD_DB_ERROR:
#             print("データベースが存在しません。")
#         else:
#             print(err)
#     else:
#         cnx.close()

#     return render_template("mysql_insert.html", **params)



# 12章の課題2　goods_tableに新しい商品データの追加が行えるプログラム
@app.route("/mysql_insert")
def challenge_mysql_insert():
    host = 'localhost'
    username = 'root'
    passwd = 'wako19980207'
    dbname = 'my_database'

    message = ""
    order = ""
    price_order = ""
    

    if "order" in request.args.keys() and "price_order" in request.args.keys() :
            order = request.args.get("order")
            price_order = request.args.get("price_order")

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        query = "select goods_name, price from goods_table"

        if order == "" and price_order == "":
            cursor.execute(query)
            print("値が入ってないので実行できない")
            message = '実行できません'

        elif order.isdecimal() != True and price_order.isdecimal() == True:
            query2 = f"INSERT INTO goods_table (goods_name, price) values ('{order}', {price_order}) " 
            cursor.execute(query2)
            cnx.commit()
 
            cursor.execute(query)
            print("商品が追加できた")
            message = '追加成功'

        else:

            cursor.execute(query)
            print("商品追加に失敗")
            message = '追加失敗'


        
        goods = []
        for (name, price) in cursor:
            item = {"name":name, "price":price}
            goods.append(item)

        params = {
        "goods" : goods,
        "message" : message
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

    return render_template("mysql_insert.html", **params)






# 13章　実習＿ひとこと掲示板
@app.route("/mysql_board")
def challenge_mysql_board():
    host = 'localhost'
    username = 'root'
    passwd = 'wako19980207'
    dbname = 'my_database'

    message = ""
    user_name = ""
    comment = ""
    sort = ""
    

    if "user_name" in request.args.keys() and "comment" in request.args.keys() :
            user_name = request.args.get("user_name")
            comment = request.args.get("comment")
            

    if "sort" in request.args.keys():
        sort = request.args.get("sort")

    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        query = "select user_name, comment, date from board_table"

        # ここが昇順、降順の条件分岐
        # if sort == 'ASC' or sort == 'DESC':
        #     sort_query = 'select user_name, comment, date from board_table order by date ' + sort
        #     cursor.execute(sort_query)
        #     print("ifが実行されている")

        # else:
        #     cursor.execute(query)
        #     print("elseが実行されている")

        if sort == 'ASC' or sort == 'DESC':
            query = 'select user_name, comment, date from board_table order by date ' + sort

        # else:
        #     query = 'select user_name, comment, date from board_table'



        # ここが名前とコメントの条件分岐
        if user_name == "" and comment == "":
            cursor.execute(query)
            print("コメントと名前が入っていません")
            message = 'コメントと名前が入っていません'

        elif 1 <= len(user_name) <= 20 and 1 <= len(comment) <= 100: 
            query2 = f"INSERT INTO board_table (user_name, comment, date) values ('{user_name}', '{comment}', LOCALTIME()) " 
            cursor.execute(query2)
            cnx.commit()

            cursor.execute(query)
            print("コメントすることに成功")
            message = 'コメントすることに成功'

        else:

            cursor.execute(query)
            print("コメントすることに失敗")
            message = 'コメントすることに失敗'  




        # 名前とコメントには必ず文字が入力されるらしい、つまり数字は弾くということ？
        # そんな掲示板あるか？笑
        # if user_name == "" and comment == "":
        #     cursor.execute(query)
        #     print("コメントと名前が入っていません")
        #     message = 'コメントと名前が入っていません'

        # elif len(user_name) <= 20 and len(comment) <= 100: 
        #     query2 = f"INSERT INTO board_table (user_name, comment, date) values ('{user_name}', '{comment}', LOCALTIME()) " 
        #     cursor.execute(query2)
        #     cnx.commit()
 
        #     cursor.execute(query)
        #     print("コメントすることに成功")
        #     message = 'コメントすることに成功'

        # else:

        #     cursor.execute(query)
        #     print("コメントすることに失敗")
        #     message = 'コメントすることに失敗'

        # sort_query = 'select user_name, comment, date from board_table order by date ' + sort
        # cursor.execute(sort_query)

        
        # ここの配列は変えて良いと思う、goodsはおかしいでしょw
        goods = []
        for (name, comment, date) in cursor:
            item = {"name":name, "comment":comment, "date":date}
            goods.append(item)

        params = {
        "goods" : goods,
        "message" : message,
        "asc_check" : sort == "ASC",
        "desc_check" : sort == "DESC"
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

    return render_template("mysql_board.html", **params)



# 14章 正規表現
import re
@app.route("/regrep", methods=['GET', 'POST'])
def regrep():
    message = ""
    phone_number = ""
    if "phone_number" in request.form.keys():
        phone_number = request.form["phone_number"]

        if len(phone_number)==0 :
            message = '携帯電話番号を入力してください。'
        elif re.match('^[0-9]{3}-[0-9]{4}-[0-9]{4}$', phone_number):
            message = 'あなたの携帯電話番号は「' + phone_number + '」です'
        else:
            message = '形式が違います。xxx-xxxx-xxxxの形式の数値で入力してください'

    return render_template('regrep.html', phone_number=phone_number, message=message)


# 14章  正規表現　課題1
@app.route("/regex_signup", methods=['GET', 'POST'])
def regex_signup():

    mail = ""
    password = ""
    message = ""
    
    if "mail" in request.form.keys() and "password" in request.form.keys():
        mail = request.form["mail"]
        password = request.form["password"]

    if len(mail)==0 and len(password)==0:
        message = 'メールアドレスとパスワードを入力してください。'

    elif re.search('[a-z0-9]@[a-z]', mail) and re.fullmatch('^[a-zA-Z0-9]{6,18}$', password):
        message = '登録完了'
    
    else:
        message = 'メールアドレスの形式が正しくありません、パスワードは半角英数記号６文字以上18文字以下で入力してください'

    return render_template('regex_signup.html', mail=mail, password=password, message=message)
    


# トランザクション　サンプル

import datetime
@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'wako19980207'    # MySQLのパスワード
    dbname   = 'my_database'    # データベース名
    customer_id = 1        # 例題のため顧客は1に固定
    payment = 'クレジット'   # 例題のため購入方法はクレジットに固定する
    quantity = 1           # 例題のため数量は1に固定
    goods = []
    cnx = None
    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()
        order = ""
        goods_id = ""
        if "goods_id" in request.form.keys() :
            goods_id = request.form["goods_id"]
        
            try:
                date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                sql = "INSERT INTO order_table (customer_id, order_date, payment) VALUES({}, '{}', '{}')".format(customer_id, date, payment)
                cursor.execute(sql)
                order_id = cursor.lastrowid # insertした値を取得できます。

                sql = "INSERT INTO order_detail_table (order_id, goods_id, quantity) VALUES({}, {}, {})".format(order_id, goods_id, quantity)
                cursor.execute(sql)

                cnx.commit()

            except mysql.connector.Error:
                cnx.rollback()
                raise

        sql = 'SELECT goods_id, goods_name, price FROM goods_table'
        cursor.execute(sql)

        for (goods_id, goods_name, price) in cursor:
            item = {"id": goods_id, "name": goods_name, "price":price}
            goods.append(item)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    finally:
        if cnx != None:
            cnx.close()

    return render_template("transaction.html", goods=goods)



# 18章　自動販売機
import os
from PIL import Image

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/ronaka/Desktop/myproject/static/'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS = {'png', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

host = 'localhost' # データベースのホスト名又はIPアドレス
username = 'root'  # MySQLのユーザ名
passwd   = 'wako19980207'    # MySQLのパスワード
dbname   = 'my_database'    # データベース名

# DBに接続する機能を関数化
# def connector_db():
#     cnx = mysql.connector.connect(host=HOST, user=USERNAME, password=PASSWD, database=DBNAME)
#     cursor = cnx.cursor()
#     return cursor

# 追加：在庫数変更のエラーメッセージ
def add_stock_error_message(stock):
    stock_error_message = "" if re.search('[0-9]', stock) else "在庫数は0以上の整数しか入れられないよ"
    return stock_error_message

# 在庫数変更のリクエストを受けた際、エラーメッセージの表示を関数化
def get_stock_change(request):
    stock = ""
    drink_id = ""
    stock_error_message = ""
    if "stock" in request.form.keys() and "drink_id" in request.form.keys():
        stock = request.form["stock"]
        drink_id = request.form["drink_id"]
        stock_error_message = add_stock_error_message(stock)
    return stock_error_message

# 公開非公開のリクエストを受けた際、変数をint化する
def cast_change_status_to_int(request):
    if "change_status" in request.form.keys() and "status_drink_id" in request.form.keys():
        change_status = int(request.form["change_status"])
        status_drink_id = int(request.form["status_drink_id"])
        return change_status, status_drink_id
    # change_status = int(request.form.get("change_status", ""))
    # status_drink_id = int(request.form.get("status_drink_id", ""))
    # return change_status, status_drink_id

# 新規に商品追加リクエストを受けた際

# 画像を保存する機能を関数化してみる
def save_image(filename):
    add_error_message = ""
    if filename == "" or filename == None:
        image = ""
        add_error_message = "名前、値段、個数、画像のどれか入力されてないよ"
        return add_error_message
    else:
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return add_error_message

# DB接続
cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
cursor = cnx.cursor()

products = []
for (image, drink_id, drink_name, price, stock, publication_status) in cursor:
    item = {"image":image, "drink_id":drink_id, "drink_name":drink_name, "price":price, "stock":stock, "publication_status":publication_status}
    products.append(item)

params = {
"products" : products,
# "add_error_message" : add_error_message,
# "success_message" : success_message,
# "status_error_message" : status_error_message,
# "stock_error_message" : stock_error_message,
# "price_error_message" : price_error_message
}



def screen_display(drink_name):
    cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    product_information = "SELECT drink_table.image, drink_table.drink_id, drink_name, price, stock, publication_status FROM drink_table JOIN stock_table ON drink_table.drink_id = stock_table.drink_id"
    if drink_name == "" or price == "" or stock == "" or image == "":
        cursor.execute(product_information)
        print('何もformから値を送信していないよ')
        print("もしくはエラーメッセージを表示？")
        return
        # return cursor.execute(product_information)



@app.route("/root")
def vending_machine_root():
    cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
    cursor = cnx.cursor()
    drink_name = ""
    screen_display(drink_name)
    # product_information = "SELECT drink_table.image, drink_table.drink_id, drink_name, price, stock, publication_status FROM drink_table JOIN stock_table ON drink_table.drink_id = stock_table.drink_id"
    # if drink_name == "" or price == "" or stock == "" or image == "":
    #     cursor.execute(product_information)

    products = []
    for (image, drink_id, drink_name, price, stock, publication_status) in cursor:
        item = {"image":image, "drink_id":drink_id, "drink_name":drink_name, "price":price, "stock":stock, "publication_status":publication_status}
        products.append(item)

    params = {
    "products" : products
    }
    return render_template("vending_machine_admin.html", **params)

        


@app.route("/vending_machine_admin", methods=["GET", "POST"])
def vending_machine_admin():
    # host = 'localhost' # データベースのホスト名又はIPアドレス
    # username = 'root'  # MySQLのユーザ名
    # passwd   = 'wako19980207'    # MySQLのパスワード
    # dbname   = 'my_database'    # データベース名


    drink_id = ""

    filename = ""

    aaaa = ""
    status_drink_id = ""
    change_status = ""
    add_error_message = ""
    add_drink_button = ""
    success_message = ""
    status_error_message = ""
    stock_error_message = ""
    price_error_message = ""

    drink_name = ""
    price = ""
    stock = ""
    image = ""
    status = ""

    # 在庫数変更の場合のみ実行
    stock_error_message = get_stock_change(request)

    result = cast_change_status_to_int(request)
    change_status = result[0] if result != None else ""
    status_drink_id = result[1] if result != None else ""
    # change_status = result[0]
    # status_drink_id = result[1]

    if  "drink_name" in request.form.keys() and "price" in request.form.keys() and "stock" in request.form.keys() and "image" in request.files and "status_selector" in request.form.keys():
        drink_name = request.form["drink_name"]
        price = request.form["price"]

        price_error_message = "" if re.search('[0-9]', price) else "値段は0以上の整数しか入れられないよ"

        # if re.search('[0-9]', price):
        #     price_error_message = ""
        # else:
        #     price_error_message = "値段は０以上の整数しか入れられないよ"


        stock = request.form["stock"]

        # if re.search('[0-9]', stock):
        #     stock_error_message = ""
        # else:
        #     stock_error_message = "在庫数は０以上の整数しか入れられないよ"

        stock_error_message = add_stock_error_message(stock)


        # image = request.files["image"]


        # statusに0,1,""の値が入る予定
        status = request.form["status_selector"]

        # if status == "" or status == None:
        #     status_error_message = "公開非公開を選択しろ"
        # else:
        #     status_error_message = ""

        status_error_message = "公開非公開を選択しろ" if status == "" or status == None else ""
        
        image = request.files["image"]
        filename = secure_filename(image.filename)
        add_error_message = save_image(filename)
        

    else:
        aaaa = ""


        # if filename == "" or filename == None:
        #     image = ""
        #     add_error_message = "名前、値段、個数、画像のどれか入力されてないよ"
        # # これでformから受け取った画像を保存する
        # else:
        #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    # elif "stock" in request.form.keys() and "drink_id" in request.form.keys():
    #     stock = request.form["stock"]
    #     drink_id = request.form["drink_id"]

    #     stock_error_message = "" if re.search('[0-9]', stock) else "在庫数は0以上の整数しか入れられないよ"

    # stock_error_message = get_stock_change(request):

        # if re.search('[0-9]', stock):
        #     stock_error_message = ""
        # else:
        #     stock_error_message = "在庫数は０以上の整数しか入れられないよ"

    # elif "change_status" in request.form.keys() and "status_drink_id" in request.form.keys():
    #     change_status = int(request.form["change_status"])
    #     status_drink_id = int(request.form["status_drink_id"])

    # result = cast_change_status_to_int(request)
    # change_status = result[0]
    # status_drink_id = result[1]
    


    # else:
    #     add_error_message = ""

    try:
        # cursor = connector_db()
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()

        # ここにtableに入れるデータの変数を書き込む
        sql_img = "./static/" + filename

        product_information = "SELECT drink_table.image, drink_table.drink_id, drink_name, price, stock, publication_status FROM drink_table JOIN stock_table ON drink_table.drink_id = stock_table.drink_id"
        # add_product = f"INSERT INTO drink_table (drink_name, price, create_day, image) VALUES ('{drink_name}', '{price}', LOCALTIME(), '{sql_img}')"
        add_product = f"INSERT INTO drink_table (drink_name, price, create_day, update_day, image, publication_status) VALUES ('{drink_name}', '{price}', LOCALTIME(), LOCALTIME(), '{sql_img}', '{status}')"
        add_product_stock = f"INSERT INTO stock_table (stock, create_day, update_day) VALUES ('{stock}', LOCALTIME(), LOCALTIME())"
        # このstock_updateが元のコード
        stock_update = f"UPDATE stock_table SET stock = '{stock}', update_day = LOCALTIME() WHERE drink_id = '{drink_id}' "

        
        change_status_private = f"UPDATE drink_table SET publication_status = 0 WHERE drink_id = {status_drink_id} "
        change_status_public = f"UPDATE drink_table SET publication_status = 1 WHERE drink_id = {status_drink_id} "



        if re.search('[0-9]', stock) and re.search('[0-9]', drink_id):
            cursor.execute(stock_update)
            cnx.commit()
            cursor.execute(product_information)
            success_message = "在庫数変更成功"
            print('在庫数変更の条件分岐がうまくいっている')

        # 公開、非公開
        elif change_status == 1 and status_drink_id != "":
            cursor.execute(change_status_private)
            cnx.commit()
            cursor.execute(product_information)
            success_message = "非公開にしたよ"
            print("非公開にすることができた")

        elif change_status == 0 and status_drink_id != "":
            cursor.execute(change_status_public)
            cnx.commit()
            cursor.execute(product_information)
            success_message = "公開成功！"
            print("公開することができた")
            

        # elif drink_name == "" and price == "" and stock == "" and image == "":
        elif drink_name == "" or price == "" or stock == "" or image == "":
            cursor.execute(product_information)
            print('何もformから値を送信していないよ')
            print("もしくはエラーメッセージを表示？")

        


        else:
            cursor.execute(add_product)
            cursor.execute(add_product_stock)
            cnx.commit()
            cursor.execute(product_information)
            success_message = "商品の追加成功"
            print('商品の追加ができて、一覧に反映されているはずだよ')


        products = []
        for (image, drink_id, drink_name, price, stock, publication_status) in cursor:
            item = {"image":image, "drink_id":drink_id, "drink_name":drink_name, "price":price, "stock":stock, "publication_status":publication_status}
            products.append(item)


        params = {
        "products" : products,
        "add_error_message" : add_error_message,
        "success_message" : success_message,
        "status_error_message" : status_error_message,
        "stock_error_message" : stock_error_message,
        "price_error_message" : price_error_message
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

    return render_template("vending_machine_admin.html", **params)




# 購入者画面のロジック　
@app.route("/vending_machine_buy", methods=["GET", "POST"])
def vending_machine_buy():
    host = 'localhost' # データベースのホスト名又はIPアドレス
    username = 'root'  # MySQLのユーザ名
    passwd   = 'wako19980207'    # MySQLのパスワード
    dbname   = 'my_database'    # データベース名

    money = ""
    change = ""
    product_price = ""
    drink_price = ""
    drink_change = ""
    select_button = ""
    drink_bought_error = ""
    my_money_error_message = ""

    if "money" in request.form.keys() and "select_button" in request.form.keys():
        money = request.form["money"]
        select_button = request.form["select_button"]

        if re.search("[0-9]", money):
            money = int(money)
        else:
            money = ""

    
    elif money == "" or re.search('0-9', money) and "select_button" in request.form.keys():
        
        money_error_message = "お金入れてねーぞ！金払え！"

    else:
        drink_bought_error = ""

    if select_button != "" and select_button != None:
        select_button = int(select_button)

    # if money != "" and money != None:
    #     money = int(money)

    # if re.search('0-9', money):
    #     money = int(money)
    
    else:
        my_money_error_message = ""

        # ここにおつりが出るロジックを書く
        # drink_change = int(money) - int(price)


    try:
        cnx = mysql.connector.connect(host=host, user=username, password=passwd, database=dbname)
        cursor = cnx.cursor()


        product_information = "SELECT drink_table.drink_id, image, drink_name, price, stock, publication_status FROM drink_table JOIN stock_table ON drink_table.drink_id = stock_table.drink_id"

        # stock_delete = f"UPDATE stock_table SET stock = '{product_stock_delete}', update_day = LOCALTIME() WHERE drink_id = '{select_button}' "

        cursor.execute(product_information)

        # stock_update = f"UPDATE stock_table SET stock = '{stock}', update_day = LOCALTIME() WHERE drink_id = '{drink_id}' "

        # もしformで送ったmoney変数に値がない場合、実行
        # if money == "":
            
            # cursor.execute(product_information)

        # もしformで送った金額に値が入っていれば、実行
        # else:

        #     products = []

        #     params = {
        #     "products" : products
        #     }
        #     return render_template("vending_machine_result.html", **params)
            # cursor.execute(product_information)

        products = []
        bought = []
        money_error_message = ""
        # bought = ""
        for (drink_id, image, drink_name, price, stock, publication_status) in cursor:
            item = {"drink_id":drink_id, "image":image, "drink_name":drink_name, "price":price, "stock":stock, "publication_status":publication_status}
            products.append(item)

            if money == "" and select_button != "":
                money_error_message = "お金入れてねーぞ！金払え！"


            
            if money != "" and item["drink_id"] == select_button:
            # if re.search('[0-9]', money) and item["drink_id"] == select_button:
                bought.append(item)
                # bought = item


                # お釣りの計算をしている
                bought_drink_all = bought[0]
                product_price = bought_drink_all["price"]
                drink_change = money - product_price

                if drink_change >= 0:
                    print("お釣りは0円以上")
                else:
                    money = ""
                print("お釣りの計算ができている？")

                

                product_stock = bought_drink_all["stock"]
                product_stock_delete = product_stock - 1
                

        # params = {
        # "products" : products,
        # "bought" : bought
        # }

        # if money != "":
        # if re.search('[0-9]', money) and select_button != "":
        if money != "" and select_button != "":
            params = {
            "bought" : bought,
            "drink_change" : drink_change
            }

            # 在庫数を減らす
            stock_delete = f"UPDATE stock_table SET stock = {product_stock_delete}, update_day = LOCALTIME() WHERE drink_id = {select_button} "
            cursor.execute(stock_delete)
            # 購入した記録をする
            purchase_record = f"INSERT INTO bought_table (drink_id, bought_day) VALUES ('{select_button}', LOCALTIME()) "
            cursor.execute(purchase_record)

            cnx.commit()
            
            return render_template("vending_machine_result.html", **params)

        elif money == "" and select_button == "":
            params = {
            "products" : products,
            "bought" : bought,
            "drink_bought_error" : drink_bought_error
            }

            return render_template("vending_machine_buy.html", **params)


        else:
            params = {
            "products" : products,
            "bought" : bought,
            "money_error_message" : money_error_message,
            "my_money_error_message" : my_money_error_message
            }

            return render_template("vending_machine_buy.html", **params)


    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("ユーザ名かパスワードに問題があります。")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("データベースが存在しません。")
        else:
            print(err)
    else:
        cnx.close()

    return render_template("vending_machine_buy.html", **params)