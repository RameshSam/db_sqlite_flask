
import cv2 , sqlite3 , os , numpy as np , face_recognition as fr , shutil
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
# from models import database
from models.Database_orm import database , Person_Details , Session , take_photo


def Convert(temp , temp2):
    try :
        os.system("cd D:/Project/DB_Image")
    except:
        parent = f"{os.getcwd()}/"
        path = os.path.join(parent , "DB_Image")
        os.mkdir(path)
    finally :
        filename = f"{os.getcwd()}/DB_Image/{temp}.jpg"
        with open(filename,"wb") as f:
            img = f.write(temp2)
        f.close()
        print(" Successfully decoded ")
    return filename

def unload():
    with sqlite3.connect("var/mydb.db") as conn:
        cur = conn.cursor()
        val = cur.execute(" SELECT * FROM Image_Table ")
        for x in val:
            name = x[2]
            img_Db = Convert(name, x[1])
        conn.commit()
        print(" Successfully Img Retrived ")
        cur.close()
    conn.close()
    return img_Db

img_name = unload()
test_img = f"{os.getcwd()}/Image/test.jpg"

# First Image

#original_img=fr.load_image_file('1.jpg')

original_img=fr.load_image_file(img_name)
original_img_rgb = cv2.cvtColor(original_img,cv2.COLOR_BGR2RGB)
copy = original_img_rgb.copy()
face = fr.face_locations(original_img_rgb)[0] 
cv2.rectangle(copy, (face[3], face[0]),(face[1], face[2]), (0,0,255), 2)
cv2.imshow('Orginal rgb', copy)
cv2.imshow('ElonMask Orginal ',original_img_rgb)
cv2.waitKey(0)


# Original Image from local 

# Second Image 

demo_img_bgr = fr.load_image_file(test_img)
emo_img_rgb = cv2.cvtColor(demo_img_bgr,cv2.COLOR_BGR2RGB)
original_face = fr.face_locations(demo_img_bgr)[0] 
demo_train_encode = fr.face_encodings(demo_img_bgr)[0]
cv2.imshow('Duplicate rgb', emo_img_rgb)
cv2.rectangle(emo_img_rgb, (face[3], face[0]),(face[1], face[2]), (0,0,255), 6)
cv2.imshow('ElonMusk Duplicate', emo_img_rgb)
cv2.waitKey(0)

# compare Faces of Encodings 

demo_encode = fr.face_encodings(original_img_rgb)[0] 
print(fr.compare_faces([demo_train_encode],demo_encode))

# clear all image of Directory 

fpath = f"{os.getcwd()}/DB_Image"
shutil.rmtree(fpath)
print("Directory Deleted ")
