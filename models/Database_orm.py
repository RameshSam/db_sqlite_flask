from sqlalchemy import create_engine , Column , ForeignKey , String , Integer , CHAR , LargeBinary
# from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker , declarative_base
from tkinter import * 
from tkinter import filedialog
import os , cv2

Base = declarative_base()

def SelectBox():
    global get_image
    get_image = filedialog.askopenfilenames(title="SELECT IMAGE", filetypes=( ("png", "*.png"), ("jpg" , "*.jpg")))

def ConvertImage_(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
        print(" Image Decoded Successfully")
    return photo_image

def InsertImage_(Variable):
        type = Variable.reg
        global s
        for image in get_image:
            E=Store_Image(ConvertImage_(image),type)
        s.add(E)
        s.commit()

class Person_Details(Base):
    __tablename__ = "Empolyee"
    reg = Column("reg",Integer,primary_key =True)
    name = Column("name",String(50),nullable=False,unique=False)
    email = Column("email",String(100),nullable=False,unique=False)
    password = Column("password",String(50),nullable=False,unique=False)

    def __init__(self , reg , name , email , password):
        self.reg = reg
        self.name = name
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f" ({self.reg}) Name : {self.name} Email_Id : {self.email} (Password : {self.password})"

class Store_Image(Base):
    __tablename__ = "Image_Table"
    Img_id = Column("Img_Id" , Integer , primary_key= True)
    img = Column(LargeBinary)
    reg = Column("reg", Integer , ForeignKey("Empolyee.reg"))

    def __init__(self , img , reg):
        self.img = img
        self.reg = reg 

    def __repr__(self):
        list_ = []
        list_.append(self.img)
        list_.append(self.reg)
        return list_
     
path = f"sqlite:///{os.getcwd()}/var/mydb.db"
engine = create_engine(path,echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()

def database(temp):
    Tkinter_Root = Tk()
    select_image = Button(Tkinter_Root, text="Select Image", command=SelectBox ,)
    select_image.grid(row=0, column=0, pady=(100, 0), padx=100)

    save_image = Button(Tkinter_Root, text="Save", command=lambda : InsertImage_(temp))
    save_image.grid(row=2, column=0)

    Tkinter_Root.mainloop()

def take_photo():

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Take Image")

    img_counter = 0

    while True:
        ret, frame = cam.read()
        cv2.imshow("Take Image", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Terminal Closed")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "Image\{}.jpg".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()



# p = Person_Details(11 ,"John", "Josarun1601@gmail.com" , 3235)
# # # p = Person_Details(12 ,"Sam", "Josarun1601@gmail.com" , 3235)
# s.add(p)
# s.commit()
# database(p)
# t = Store_Image(1, "Car ", p.reg)
# t1 = Store_Image(2, "Joystick ", p1.reg)
# t2 = Store_Image(3, "Muscale", p2.reg)
# t3 = Store_Image(4, "Description ", p3.reg)
# t4 = Store_Image(5, "Store_Image ", p4.reg)

# s.add(t)
# s.add(t1)
# s.add(t2)
# s.add(t3)
# s.add(t4)
# s.commit()

# result = s.query(Store_Image).all()
# # print(result)
# for i in result:
#     print(i)
    
# result = s.query(Store_Image,Person_Details).all()
# # print(result)
# for i in result:
#     print(i)

