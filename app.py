from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2

app=Flask(__name__)
# database connection

url="postgres://twnmwpyf:p76FuD9GIzdYAxry-PAbZtQFfAm2XU51@queenie.db.elephantsql.com/twnmwpyf"
connection=psycopg2.connect(url)

# for creating new table
#
# with connection:
#     with connection.cursor()as cursor:
#         cursor.execute("CREATE TABLE coupons(CouponID INT UNIQUE,CouponTitle TEXT NOT NULL,StartDate timestamp,EndDate timestamp,Location TEXT  NOT NULL);")


# home
@app.route("/")
def home():
	return "Coupon Add"

# add coupon
@app.route('/couponadd',methods=['POST'])
def add_coupon():
    data=request.get_json()
    ID=data["CouponID"]
    Title=data["CouponTitle"]
    StartDate=data["StartDate"]
    EndDate=data["EndDate"]
    Location=data["Location"]
    if  Title == ""or  Location =="":
        return {"NULl": "Location and Coupon Title can't be null"}
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO coupons VALUES(%s ,%s, %s, %s, %s);",(ID,Title,StartDate,EndDate,Location))
                return "Added!"
    except (connection.Error, connection.Warning) as e:
        print(e)
        return str(e)

# show all coupon
@app.route('/showcoupon')
def show_coupons():
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM coupons;")
                transactions=cursor.fetchall()
        return jsonify({"results":transactions})
    except (connection.Error, connection.Warning) as e:
        print(e)
        return str(e)

#show specific coupon
@app.route('/showcoupon/<id>')
def show_coupon(id):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM coupons WHERE couponid = "+id+";")
                transactions=cursor.fetchall()
        if transactions:
            return jsonify({"results":transactions})
        else:
            return jsonify({"results":"No Match"})
    except (connection.Error, connection.Warning) as e:
        print(e)
        return str(e)



port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(port)
