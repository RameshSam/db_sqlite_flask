from sqlalchemy import create_engine , Column , LargeBinary , String , Integer 
from sqlalchemy.orm import sessionmaker , declarative_base 
import os

Base = declarative_base()

class Store(Base):
    __tablename__ = "Store_Images"
    rid = Column("Reg_ID",Integer , primary_key= True)
    name = Column("Name", String , nullable=False)
    img = Column("Image" , LargeBinary )

    def __init__(self, name , img):
        self.name = name 
        self.img = img

    def __repr__(self):
        return f"{self.name} {self.img}"
    
path = f"sqlite:///{os.getcwd()}/var/mydb2.db"
engine = create_engine(path,echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
s = Session()

def ConvertImage_(filename):
    with open(filename, 'rb') as file:
        photo_image = file.read()
        print(" Image Decoded Successfully")
    return photo_image

img_list = []
img_path = f"{os.getcwd()}/Image"
for file in os.listdir(img_path):
    if file.endswith(".jpg") or file.endswith(".png") :
        img_list.append(file)
print(img_list)
for f in img_list:
    filename = f.split(".")
    imgf = f"{img_path}/{f}"
    print(filename[0])
    print(imgf)
    p = Store(str(filename[0]),ConvertImage_(imgf))
    s.add(p)
s.commit()