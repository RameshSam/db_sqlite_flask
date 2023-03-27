
from tkinter import * 
from tkinter import filedialog
from flask import Flask
from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy 
from datetime import timedelta
import os 

app = Flask(__name__)
path = f"sqlite:///{os.getcwd()}/var/sample_img.db"
app.config["SQLALCHEMY_DATABASE_URI"] = path
app.config["SQLALCHEMY_TRACK_MDODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)
global db
db = SQLAlchemy()
db.init_app(app)

def SelectBox():
    global get_image
    get_image = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=( ("png", "*.png"), ("jpg" , "*.jpg")))

def ConvertImage_(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
        print(" Image Loaded Successfully ")
    return photo_image

def InsertImage_():
    global app
    with app.app_context():
        db.create_all()
        for image in get_image:
            E=ExampleTable("sam",ConvertImage_(image))
        db.session.add(E)
        db.session.commit()

def database():
    Tkinter_Root = Tk()

    select_image = Button(Tkinter_Root, text="Select Image", command=SelectBox)
    select_image.grid(row=0, column=0, pady=(100, 0), padx=100)

    save_image = Button(Tkinter_Root, text="Save", command=InsertImage_)
    save_image.grid(row=2, column=0)

    Tkinter_Root.mainloop()

class ExampleTable(db.Model):
    __tablename__ = "Image_Table"
    
    id_ = db.Column("id",db.Integer , primary_key = True)
    name = db.Column(db.String(50))
    img = db.Column(db.LargeBinary)

    def __init__(self, name , img):
        self.name = name 
        self.img  = img

if __name__ == "__main__":
    database()