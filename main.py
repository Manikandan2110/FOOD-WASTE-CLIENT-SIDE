import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
# connection =
app.secret_key = 'manii'
UPLOAD_FOLDER = "static/upload"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def getconnection():
    return mysql.connector.connect(user="root", database="foods")

@app.route("/matplotlib")
def matplotlib():
    connection = getconnection()
    cur = connection.cursor()
    mf=cur.execute("select substr(food_date,4,2) as entry_date,count(food_id) as food_count from food_details group by entry_date")
    result = cur.fetchall()
    res = []
    for row in result:
        dto = datetime.datetime.strptime(row[0], "%m")
        res.append([dto.strftime("%B"), row[1]])
    mu= cur.execute("SELECT COUNT(*) FROM `users`")
    result1 = cur.fetchall()
    cur.close()
    print(res)
    return render_template("matplotlib.html", data=res,data1=result1)


@app.route("/matplotlibuser")
def matplotlibuser():
    connection = getconnection()
    cur = connection.cursor()
    mu= cur.execute("SELECT COUNT(*) FROM `users`")
    result = cur.fetchall()
    cur.close()
    print(result)
    return render_template("matplotlibuser.html", data=result)


@app.route("/morebutton")
def morebutton():
    return render_template("morebutton.html")


@app.route("/usersentry")
def usersentry():
    return render_template("usersentry.html")

@app.route("/dropdown")
def dropdown():
    return render_template("dropdown.html")

@app.route("/")
def firstpage():
    return render_template("firstpage.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/foodentry")
def foodentry():
    return render_template("foodentry.html")


@app.route("/nooooo")
def nooooo():
    return render_template("nooooo.html")

@app.route("/styleheaderveg")
def styleheaderveg():
    return render_template("styleheaderveg.html")

@app.route("/styleheaderfast")
def styleheaderfast():
    return render_template("styleheaderfast.html")

@app.route("/myorderstable")
def myorderstable():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("SELECT u.users_id, u.users_photo, u.users_name, u.users_address, u.users_phno, f.food_id, f.food_name, f.food_photo, f.food_type1, f.food_type2, f.food_date, f.food_time, o.order_orderid, o.order_approve from orders as o JOIN users as u on u.users_id = o.order_buyerid JOIN food_details as f on f.food_id WHERE o.order_userid=%s", (id,))
    result = cur.fetchall()
    print(result)
    cur.close()
    return render_template("myorderstable.html", data=result)


@app.route("/myorders")
def myorders():
    connection = getconnection()
    cur = connection.cursor()
    id = session['users_id']
    cur.execute("SELECT u.users_id, u.users_photo, u.users_name, u.users_address, u.users_phno, f.food_id, f.food_name, f.food_photo, f.food_type1, f.food_type2, f.food_date, f.food_time, o.order_orderid, o.order_approve from orders as o JOIN users as u on u.users_id = o.order_userid JOIN food_details as f on f.food_id=o.order_foodid WHERE o.order_buyerid=%s", (id,))
    result = cur.fetchall()
    print(result)
    cur.close()
    return render_template("myorders.html", data=result)

@app.route("/ordersentry")
def ordersentry():
    return render_template("ordersentry.html")



@app.route("/foodtype")
def foodtype():
    return render_template("foodtype.html")

@app.route("/styleheader")
def styleheader():
    return render_template("styleheader.html")

@app.route("/response")
def response():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("UPDATE `orders` SET `order_approve`= 'Yes' WHERE  `order_orderid`= %s",(id,))
    connection.commit()
    cur.close()
    return render_template("response.html")

@app.route("/cancelorder")
def cancelOrder():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("UPDATE `orders` SET `order_approve`= 'No' WHERE  `order_orderid`= %s",(id,))
    connection.commit()
    cur.close()
    return render_template("cancelorder.html")



@app.route("/request")
def requestOrders():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("SELECT u.users_id, u.users_photo, u.users_name, u.users_address, u.users_phno, f.food_id, f.food_name, f.food_photo, f.food_type1, f.food_type2, f.food_date, f.food_time, o.order_orderid, o.order_approve from orders as o JOIN users as u on u.users_id = o.order_buyerid JOIN food_details as f on f.food_id=o.order_foodid WHERE o.order_approve!='Yes' AND o.order_userid=%s", (id,))
    result = cur.fetchall()
    cur.close()
    return render_template("request.html", data=result)

@app.route("/currentresponse")
def currentResponse():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("SELECT u.users_id, u.users_photo, u.users_name, u.users_address, u.users_phno, f.food_id, f.food_name, f.food_photo, f.food_type1, f.food_type2, f.food_date, f.food_time, o.order_orderid, o.order_approve from orders as o JOIN users as u on u.users_id = o.order_buyerid JOIN food_details as f on f.food_id=o.order_foodid WHERE o.order_approve='Yes' AND o.order_userid=%s", (id,))
    result = cur.fetchall()
    cur.close()
    return render_template("currentresponse.html", data=result)



@app.route("/header")
def header():
    connection = getconnection()
    cur = connection.cursor()
    id = session['users_id']
    a = cur.execute("SELECT COUNT(*) FROM  orders WHERE order_buyerid=%s",(id,))
    result = cur.fetchall()
    b = cur.execute("SELECT COUNT(*) FROM orders WHERE order_approve!='yes' and order_userid=%s",(id,))
    result1 = cur.fetchall()
    print(id)
    c = cur.execute("SELECT COUNT(*) FROM orders WHERE order_approve='yes' and order_userid=%s",(id,))
    result2 = cur.fetchall()
    cur.close()
    print(result)
    print(result1)
    print(result2)
    return render_template("header.html", total=result[0][0],total1=result1[0][0],total2=result2[0][0])

@app.route("/responsetable")
def responsetable():
    connection = getconnection()
    cur = connection.cursor()
    id = request.args.get("RN")
    cur.execute("SELECT u.users_id, u.users_photo, u.users_name, u.users_address, u.users_phno, f.food_id, f.food_name, f.food_photo, f.food_type1, f.food_type2, f.food_date, f.food_time, o.order_orderid,o.order_approve from orders as o JOIN users as u on u.users_id = o.order_userid JOIN food_details as f on f.food_id=o.order_foodid WHERE o.order_buyerid=%s", (id,))
    result = cur.fetchall()
    cur.close()
    return render_template("responsetable.html", data=result)


@app.route("/food_detailsveg")
def food_detailsveg():
    id = session["users_id"]
    connection = getconnection()
    cur = connection.cursor()
    cur.execute( "SELECT fd.*, u.* FROM food_details fd INNER JOIN users u ON fd.users_id = u.users_id WHERE fd.users_id != %s AND fd.food_type1 ='Veg' AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_userid =%s)AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_approve = 'Yes')",(id, id,))
    result = cur.fetchall()
    print(result)
    cur.close()
    return render_template("food_detailsveg.html", data=result)



@app.route("/jointable")
def jointable():
    id = session["users_id"]
    connection = getconnection()
    cur = connection.cursor()
    cur.execute("SELECT fd.*, u.* FROM food_details fd INNER JOIN users u ON fd.users_id = u.users_id WHERE fd.users_id != %s AND fd.food_type1 = 'Non Veg' AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_userid =%s)AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_approve = 'Yes')", (id,id,))
    result = cur.fetchall()
    print(result)
    cur.close()
    return render_template("food_detailsnonveg.html", data=result)

@app.route("/food_detailsfast")
def food_detailsfast():
    id = session["users_id"]
    connection = getconnection()
    cur = connection.cursor()
    cur.execute("SELECT fd.*, u.* FROM food_details fd INNER JOIN users u ON fd.users_id = u.users_id WHERE fd.users_id != %s AND fd.food_type1 = 'Fast' AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_userid =%s)AND fd.food_id NOT IN (SELECT o.order_foodid FROM orders o WHERE o.order_approve = 'Yes')", (id, id,))
    result = cur.fetchall()
    print(result)
    cur.close()
    return render_template("food_detailsfast.html", data=result)

@app.route("/loginform", methods =["POST","GET"])
def loginform():
    connection = getconnection()
    cur = connection.cursor()
    if request:
        em=request.form["users_email"]
        ps=request.form["users_password"]
    cur.execute("select * from users where users_email='"+em+"' and users_password='"+ps+"'")
    result = cur.fetchone()
    cur.close()
    if result:
        session["user"]=em
        session["users_id"] = result[1]
        session["users_name"] = result[2]
        session["users_photo"] = result[0]
        return redirect(url_for("header"))
    else:
        return render_template("header.html")




@app.route("/users")
def users():
    connection = getconnection()
    cur = connection.cursor()
    cur.execute("select * from users")
    result = cur.fetchall()
    cur.close()
    return render_template("users.html", data=result)

@app.route("/usersSave", methods =["POST","GET"])
def usersSave():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        a = file.filename
        b = request.form["users_id"]
        c = request.form["users_name"]
        d = request.form["users_address"]
        e = request.form["users_email"]
        f = request.form["users_password"]
        g = request.form["users_sex"]
        h = request.form["users_phno"]
        i = request.form["users_state"]
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("insert into users values('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"')")
        connection.commit()
        return redirect(url_for("firstpage"))


@app.route("/usersdelete", methods =["POST", "GET"])
def usersdelete():
        id = request.args.get("RN")
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("delete from  users where users_photo='"+id+"'")
        connection.commit()
        cur.close()
        return redirect(url_for("users"))

@app.route("/food_details")
def food_details():
    connection = getconnection()
    cur = connection.cursor()
    cur.execute("select * from food_details")
    result = cur.fetchall()
    cur.close()
    return render_template("food_details.html", data=result)

@app.route("/food_detailsSave", methods =["POST","GET"])
def food_detailsSave():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        a = request.form["users_id"]
        b = request.form["food_id"]
        c = request.form["food_type1"]
        d = request.form["food_type2"]
        e = request.form["food_name"]
        f = request.form["food_date"]
        g = request.form["food_time"]
        h = request.form["food_location1"]
        i = request.form["food_location2"]
        j = request.form["food_phono"]
        k = file.filename
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("insert into food_details values('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"','"+g+"','"+h+"','"+i+"','"+j+"','"+k+"')")
        connection.commit()
        return redirect(url_for("header"))


@app.route("/food_detailsdelete", methods = ["POST", "GET"])
def food_detailsdelete():
        id = request.args.get("RN")
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("delete from  food_details where users_id='"+id+"'")
        connection.commit()
        cur.close()
        return redirect(url_for("food_details"))




@app.route("/orders")
def orders():
    connection = getconnection()
    cur = connection.cursor()
    cur.execute("select * from orders")
    result = cur.fetchall()
    cur.close()
    return render_template("orders.html", data=result)




@app.route("/ordersSave", methods =["POST","GET"])
def ordersSave():
    if request.method == "POST":
        a = request.form["order_userid"]
        b = request.form["order_foodid"]
        c = request.form["order_buyerid"]
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("insert into orders values('"+a+"','"+b+"','"+c+"','No',0)")
        connection.commit()
        return redirect(url_for("header"))

@app.route("/ordersdelete", methods=["POST", "GET"])
def ordersdelete():
        id = request.args.get("RN")
        connection = getconnection()
        cur = connection.cursor()
        cur.execute("delete from  orders where order_userid='"+id+"'")
        connection.commit()
        cur.close()
        return redirect(url_for("orders"))

if __name__== "__main__":
    app.run(port=8000 ,debug=True)