from flask import Flask , render_template , request
import sqlite3 , os
from models.Database_orm import database , Person_Details , Session , take_photo

s= Session()

app =Flask(__name__ , template_folder="template")

@app.route("/")
def index():
    return render_template("signup.html")

@app.route("/getdata",methods = ['GET','POST'])   
def getdata():
    if request.method == "POST" :
        try:
            global reg
            reg = request.form["Reg"]
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["pass"]


            p = Person_Details(reg , name , email ,password )
            s.add(p)
            s.commit()
            database(p)
        
            result =s.query(Person_Details).all()
            for i in result:
                print(i)
            print(" Table Showed ")
            msg = " Account Created "
        except:
            msg = "Error in Insertion of Database"
        finally:
            return render_template("result.html", msg= msg , name = name)
        
@app.route("/login")
def login():
    return render_template("signin.html")

@app.route("/getdata/takephoto")
def takephoto():
    take_photo()

@app.route("/fetchdata",methods =['GET',"POST"])
def fetchdata():
   if request.method == "POST" :
        try:
            name = request.form["name"]
            password = request.form["pass"]

            with sqlite3.connect("var/mydb.db") as conn:
                curs = conn.cursor()
                scmd = """ SELECT * FROM Empolyee ;"""
                curs.execute(scmd)
                result = curs.fetchmany()
                for i in result:
                    if ( name == i[1] and password == i[3] ):
                        msg = " Login Successfully.."
                    else :
                        msg = " Login Failed.."
                    print(i)
                print(" Table Data Allocated... ")
                conn.commit()
        except:
            conn.rollback()
            msg = "Error in Logining"

        finally:
            conn.close()
            return render_template("result.html", msg= msg )
@app.route("/change")
def change():
    return render_template("changepass.html")

@app.route("/changedata",methods =['GET',"POST"])
def changedata():
   if request.method == "POST" :
        try:
            email = request.form['email']
            curpass = request.form["curpass"]
            password = request.form["pass"]

            with sqlite3.connect("var/mydb.db") as conn:
                curs = conn.cursor()
                scmd = """ SELECT * FROM Empolyee ; """
                curs.execute(scmd)
                result = curs.fetchmany()
                for i in result:
                    if (curpass == i[3]):
                        conn.execute(" UPDATE Empolyee SET Password=(?) WHERE Email=(?)",(password , email))
                        msg = " Password Updated.."
                    else :
                        msg = " Password Update Failed.."
                curs.execute(" SELECT * FROM Empolyee ; ")
                result1 = curs.fetchmany()
                for j in result1:
                    print(j)
                print(" Table Data Updated... ")
                conn.commit()
        except:
            conn.rollback()
            msg ="Failure Updatation"
            
        finally:
            conn.close()
            return render_template("result.html", msg= msg)

if __name__ == "__main__" :
    app.run(debug=True)