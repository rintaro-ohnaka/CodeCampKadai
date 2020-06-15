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
    