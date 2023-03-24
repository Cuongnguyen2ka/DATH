import cv2
import imutils
import numpy as np
import pytesseract
import re
from mfrc522 import SimpleMFRC522
from RPLCD import i2c
import csv  #thu viện hỗ trợ dạng file excel
import pandas as pd #thư viện lưu dữ liệu ra nhiều định dạng file khác nha
from datetime import datetime

import RPi.GPIO as GPIO
import pigpio 
#importing the library of RPi.GPIO
from time import sleep
import time

from tkinter import *
import tkinter
from PIL import Image, ImageTk
from time import strftime

pi = pigpio.pi()
time1 = datetime.now()

lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27 
port = 1
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
pi.set_servo_pulsewidth(4, 500)
pi.set_servo_pulsewidth(17, 500)

servo1=4
servo2=17
button1=20
button2=21
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)

sensor0 = 16
sensor1 = 6
sensor2 = 19
sensor3 = 23

#coi
buzzer = 24

led0 = 26
led1 = 13
led2 = 5
led3 = 27



GPIO.setup(sensor0,GPIO.IN)
GPIO.setup(sensor1,GPIO.IN)
GPIO.setup(sensor2,GPIO.IN)
GPIO.setup(sensor3,GPIO.IN)
GPIO.setup(sensor3,GPIO.IN)
#set the behaviour of sensor as input

GPIO.setup(led0,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)

#coi
GPIO.setup(buzzer,GPIO.OUT)
#set the behaviour of led as output
slot=[0,0,0,0]
biensodk = ["62F-567.89","29C-999.99", "51G888.88", "93B-111.00"]
idluu = [13315121439,1006290278699, 632745730549, 1039107234715] 
#Truong hop the mat 
tenkh = ["Van A", "Van B", "Le Thi D","Khach Ngoai"]

reader = SimpleMFRC522()
camera = cv2.VideoCapture(0)
win = tkinter.Tk()
win.title("Ứng Dụng Công Nghệ RFID Và Xử Lý Ảnh Trong Bãi Giữ Xe Ô Tô Chung Cư")
win.geometry("1050x900")
win.configure(bg='#F8F8FF')
label=Label(win)
lmain = tkinter.Label(win)
lmain.pack()

def my_time():
    time_string = strftime('%d/%m/%Y') # time format 
    l1.config(text=time_string)
    l1.after(1000,my_time) # time delay of 1000 milliseconds
l1=Label(win,text ="CUA VAO",font=('times new roman', 18,'bold') ,bg='#F8F8FF', fg='blue')
l1.place(x=800, y=400)
my_time()
def cuavao():
    pi.set_servo_pulsewidth(servo1, 1500)
    time.sleep(3)
    pi.set_servo_pulsewidth(servo1, 500)
mocuavao=Button(win,text ="CONG VAO", width=10,font=("Times New Roman", 10,"bold"), bg="white", fg="black", command=cuavao)
mocuavao.place(x=10, y=380)
def cuara():
    pi.set_servo_pulsewidth(servo2, 1500)
    time.sleep(3)
    pi.set_servo_pulsewidth(servo2, 500)
mocuara=Button(win,text ="CONG RA", width=10,font=("Times New Roman", 10,"bold"), bg="white", fg="black", command=cuara)
mocuara.place(x=380, y=380)
    
diadiem = tkinter.Label(win,text="TP. Hồ Chí Minh, ", background='#F8F8FF',fg='blue', font=("Times New Roman", 18,"bold"))
diadiem.place(x=600, y=400)

label1 = tkinter.Label(win,text="Phí Gửi Xe Khách Ngoài: 5000 VNĐ", background='#F8F8FF', font=("Times New Roman", 18,"bold"), fg="red")
label1.place(x=600, y=450)

img_bg= Image.open("Logo TDTU.png")
resized_image= img_bg.resize((210,110))
bground = ImageTk.PhotoImage(resized_image)
logo = tkinter.Label(win, image=bground, bg='#F8F8FF', fg='#FF0000')
logo.place(x=680, y=10)
label1 = tkinter.Label(win,text="ĐỒ ÁN TỔNG HỢP", background='#F8F8FF', font=("Times New Roman", 18,"bold"), fg="blue")
label1.place(x=680, y=150)

label2 = tkinter.Label(win,text="ỨNG DỤNG CÔNG NGHỆ RFID \n VÀ XỬ LÝ ẢNH TRONG BÃI GIỮ XE \n Ô TÔ CHUNG CƯ", background='#F8F8FF', font=("Times New Roman", 16,"bold"), fg="blue")
label2.place(x=600, y=190)

label3 = tkinter.Label(win,text="GVHD: TS. HOÀNG THỊ HƯƠNG GIANG", background='#F8F8FF', font=("Times New Roman", 16,"bold"), fg="blue")
label3.place(x=600, y=280)

label4 = tkinter.Label(win,text="SVTH: NGUYỄN MẠNH CƯỜNG", background='#F8F8FF', font=("Times New Roman", 16,"bold"), fg="blue")
label4.place(x=600, y=310)

label5 = tkinter.Label(win,text="MSSV: 41800993", background='#F8F8FF', font=("Times New Roman", 16,"bold"), fg="blue")
label5.place(x=600, y=340)

biensoxevao = tkinter.Label(win, text="Biển số xe vào", font= ("Times New Roman",16, "bold"),bg='#F8F8FF')
biensoxevao.place(x=10, y=420)
biensoxera = tkinter.Label(win, text="Biển số xe ra", font= ("Times New Roman",16, "bold"),bg='#F8F8FF')
biensoxera.place(x=380, y=420)

slottrongbai = tkinter.Label(win, text="SLOT TRỐNG:", font= ("Times New Roman",16, "bold"),bg='#F8F8FF')
slottrongbai.place(x=600, y=480)


id = None
try:

    def show_frame():
#initiated a infinite while loop
        input_state1 = GPIO.input(button1)
        input_state2 = GPIO.input(button2)
        if input_state1 == False:
            pi.set_servo_pulsewidth(servo1, 1500)
            time.sleep(3)
            pi.set_servo_pulsewidth(servo1, 500)

        else:
            pi.set_servo_pulsewidth(servo1, 500)
        
        if input_state2 == False:
            pi.set_servo_pulsewidth(servo2, 1500)
            time.sleep(3)
            pi.set_servo_pulsewidth(servo2, 500)
            
        else:
            pi.set_servo_pulsewidth(servo2, 500)
        if (GPIO.input(sensor0)==0):
            GPIO.output(led0, True)
        else:
            GPIO.output(led0, False)

        if (GPIO.input(sensor1)==0):
            GPIO.output(led1, True)
        else:
            GPIO.output(led1, False)

        if (GPIO.input(sensor2)==0):
            GPIO.output(led2, True)
        else:
            GPIO.output(led2, False)
        if (GPIO.input(sensor3)==0):
            GPIO.output(led3, True)
        else:
            GPIO.output(led3, False)
        #led turned off if there is no input on sensor
        ret , img = camera.read()
        img = cv2.resize(img, (600, 300))      
        id = reader.read_id_no_block()
        if id == None:
            id = None
        else:
            lcd.close(clear=True)
            print(id)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
            gray = cv2.bilateralFilter(gray, 11, 17, 17)#anh nguồn, đường kính, sigmaColor, sigmaSpace
            edged = cv2.Canny(gray, 70, 100)#anhnguon, gia trị ngưỡng tối thiểu, giá trị ngưỡng tối đa
            cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#anh nguon, che độ truy xuất đường viền, chế độ xấp xỉ đường viền chỉ lấy 4 điểm góc
            cnts = imutils.grab_contours(cnts)# Camera nhận diện được đường viền ảnh dưới dạng chuỗi
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)# Sắp xếp các chuỗi số từ lớn đến bé chọn ra đường viền lớn nhất
            screenCnt = None
                
                # loop over our contours
            for c in cnts:
                #Tính chu vi từng đường viền đóng được tìm thấy ở bước trên các lệnh liên quan đến biên 
                 
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                 
                
                 # so sánh tìm ra hình chữ nhật tức biển số xe
                 # nếu approximated contour nào có 4 điểm góc thì đó là biển số xe trong bức 
                if len(approx) == 4:
                    screenCnt = approx
                    break
                
            if screenCnt is None:
                    detected = 0
                    print ("No contour detected")
                    bienso = "0"
            else:
                detected = 1
                # Vẽ biên màu xanh đóng khung đường biên tìm thấy được ở bước trên  
                cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)# anh nguon, ds cac duong vien, vẽ tất cả các đường viền, thông số màu xanh chanh(Lime), độ dày)

            # Masking the part other than the number plate # Che phần không phải là biển số
                mask = np.zeros(gray.shape,np.uint8)  # tạo 1 m trận số 0 có kích thước bằng với ảnh đã chụp bên trên 
                new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)# ds1: anh nguon, ds2: danh sach cac duong vien, ds3: chi so cua duong vien
                new_image = cv2.bitwise_and(img,img,mask=mask)#chi lay vung co chua bien so  
                (x, y) = np.where(mask == 255)
                (topx, topy) = (np.min(x), np.min(y))
                (bottomx, bottomy) = (np.max(x), np.max(y))
                Cropped = gray[topx:bottomx, topy:bottomy]
                bienso = pytesseract.image_to_string(Cropped,config='--psm 6')# psm 6 dam bao la mot khoi van ban thong nhat
                bienso = re.sub("[^-.qA-Za-z0-9]","",bienso)
                bienso = str(bienso)
                print(bienso)
                lcd.cursor_pos = (0, 0)
                lcd.write_string(bienso)
                mathe =str(id)
                lcd.cursor_pos = (3, 0)
                lcd.write_string(mathe)
                xedadk = 0
                iddadk = 0
                xehople = 0
                
            
                xeravao="xe ra"
                for j in biensodk:
                    if(bienso == j):
                        xedadk = 1
                        break
                
                for i in idluu:      
                    if  (id==i) and (xedadk == 1): 
                        a=idluu.index(id)
                        b=biensodk.index(bienso)  
                        iddadk = 1
                        if(a==b):    
                            if slot[a] == 0:
                                slot[a] = 1 

                                print("Servor 1 on")
                                #GPIO.output(buzzer, GPIO.HIGH)
                                #time.sleep(0.01) 
                                #GPIO.output(buzzer, GPIO.LOW)
                                lcd.cursor_pos = (2, 0)
                                lcd.write_string("TEN KH: "+ str(tenkh[a]))
                                
                                text1=StringVar(win, bienso)
                                xevao= tkinter.Label(win, textvariable=text1,bg='#F8F8FF',font= ("Times New Roman",14))
                                xevao.place(x=20, y=450)
                                
                                pi.set_servo_pulsewidth(servo1, 1500)
                                time.sleep(5)
                                pi.set_servo_pulsewidth(servo1, 500)
                                xeravao="xe vao"

                            else:
                                slot[a] = 0
                                print("Servor 2 on")
                                #GPIO.output(buzzer, GPIO.HIGH)
                                #time.sleep(0.01) 
                                #GPIO.output(buzzer, GPIO.LOW)
                                lcd.cursor_pos = (2, 0)
                                lcd.write_string("TEN KH: "+ str(tenkh[a]))
                                text2=StringVar(win, bienso)
                                
                                xera= tkinter.Label(win, textvariable=text2,bg='#F8F8FF',font= ("Times New Roman",14))
                                xera.place(x=390, y=450)
                                pi.set_servo_pulsewidth(servo2, 1500)
                                time.sleep(5)
                                pi.set_servo_pulsewidth(servo2, 500)
                                xeravao="xe ra"
                                                         
                             
                            xehople = 1
                            data = pd.read_csv("bienso.csv")
                            time1 = datetime.now()
                            new_row = [time1, mathe,tenkh[a],bienso,xeravao]
                            data.loc[-1] = new_row
                            data.reset_index(drop=True) # resetting index (giá trị bool và resetting  index columm dữ liệu if else)
                            data.to_csv("bienso.csv",index=False)#
                            break  

                        else:
                            
                            break  

                if (xehople == 0):
                    if( (xedadk ==1) and (iddadk ==1)):
                        print("Coi")
                        GPIO.output(buzzer, GPIO.HIGH)
                        time.sleep(2) 
                        GPIO.output(buzzer, GPIO.LOW)
                        lcd.cursor_pos = (0, 0)
                        lcd.write_string("KHONG TRUNG KHOP")

                    else:
                        GPIO.output(buzzer, GPIO.HIGH)
                        time.sleep(2) 
                        GPIO.output(buzzer, GPIO.LOW)
                        lcd.cursor_pos = (0, 0)
                        lcd.write_string("THE XE CHUA DANG KY")

                sochotrong = 0
                for i in slot:
                    if i == 0:
                        sochotrong = sochotrong+1
                        lcd.cursor_pos = (1, 0)
                        lcd.write_string("SO CHO TRONG:"+ str(sochotrong))
                        SCT=StringVar(win, sochotrong)
                        SCTconlai= tkinter.Label(win, textvariable=SCT,bg='#F8F8FF',font= ("Times New Roman",14))
                        SCTconlai.place(x=750, y=480)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk, width=550, height=400)
        lmain.after(20, show_frame)
        lmain.place(x=0, y=0)   
    show_frame()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    win.mainloop()
finally:

        GPIO.cleanup()