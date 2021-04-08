import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from random import randint
from database import insertUserInfo, insertUserLog, insertImage, selectUserInfo

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Face_Recogniser")

dialog_title = 'QUIT'
dialog_text = 'Are you sure?'
#answer = messagebox.askquestion(dialog_title, dialog_text)

window.geometry('1280x720')
window.configure(background='white')


frame = tk.LabelFrame(window, padx=50, pady=50)
frame.grid(row=3, column=0, columnspan=10)
message = tk.Label(window, text="Video Based Dynamic Human Authentication System For Access Control",
                   bg="slate grey", fg="white", width=80, height=3, font=('times', 20, ' bold underline'), borderwidth=3, relief="solid")

message.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

# lbl = tk.Label(window, text="Enter ID :", width=20, height=2,
#               fg="black", bg="light slate grey", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
#lbl.grid(row=1, column=0, padx=10, pady=10)

# txt = tk.Entry(window, width=30, bg="light slate grey",
#              fg="black", font=('times', 13, ' bold '), borderwidth=2, relief="solid")
#txt.grid(row=1, column=1, sticky="W", padx=10, pady=10)

lbl2 = tk.Label(window, text="Enter Name :", width=20, fg="black",
                bg="light slate grey", height=2, font=('times', 13, ' bold '), borderwidth=3, relief="groove")
lbl2.grid(row=2, column=0, padx=10, pady=10)

txt2 = tk.Entry(window, width=30, bg="light slate grey",
                fg="black", font=('times', 13, ' bold '), borderwidth=2, relief="solid")
txt2.grid(row=2, column=1, sticky="W", padx=10, pady=10)

lbl3 = tk.Label(window, text="Notification", width=13, fg="black",
                bg="light slate grey", height=2, font=('times', 13, ' bold'), borderwidth=3, relief="groove")
lbl3.grid(row=1, column=3, padx=10, pady=10)

message = tk.Label(window, text="", bg="light slate grey", fg="black", width=30,
                   height=2, activebackground="light slate grey", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
message.grid(row=2, column=3, padx=10, pady=10,
             sticky="E")

lbl3 = tk.Label(frame, text="UserLog", width=25, fg="black",
                bg="light slate grey", height=2, font=('times', 13, ' bold  '), borderwidth=3, relief="groove")
lbl3.grid(row=4, column=0, columnspan=4, padx=10,
          pady=10)

message2 = tk.Label(frame, text="", fg="black", bg="light slate grey",
                    activeforeground="green", width=40, height=4, font=('times', 13, ' bold '), borderwidth=3, relief="groove")
message2.grid(row=5, column=0, columnspan=4, padx=10,
              pady=10)


def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text=res)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def TakeImages():
    Id = str(randint(0, 20))
    name = (txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)  # set video width
        cam.set(4, 480)  # set video height
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # incrementing sample number
                sampleNum = sampleNum+1
                # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("dataset\ "+name + "."+Id + '.' +
                            str(sampleNum) + ".jpg", gray[y:y+h, x:x+w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]
        with open('UserInfo\\UserInfo.csv', 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        insertUserInfo(Id, name)
        message.configure(text=res)
    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text=res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text=res)


def TrainImages():
    path = 'dataset'
    # recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, Ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(Ids))
    recognizer.write("trainner\\trainner.yml")
    res = "Image Trained"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePaths)

    # create empth face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        #face = detector.detectMultiScale(imageNp)
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("trainner\\trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("UserInfo\\UserInfo.csv")
    #df=selectUserInfo()
    knownimg = 0
    unknownimg = 0
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    attendance = pd.DataFrame(columns=col_names)
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )
        for(x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), 2)
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if(conf < 85):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(
                    ts).strftime('%H:%M:%S')
                aa = df.loc[df['Id'] == Id]['Name'].values
                tt = str(Id)+"-"+aa
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                knownimg = knownimg+1
                if (knownimg <= 1):
                    noOfFile1 = len(os.listdir("Imagesknown"))+1
                    cv2.imwrite("Imagesknown\Image" +
                                str(noOfFile1) + ".jpg", im[y:y+h, x:x+w])
                    pathKnown = os.path.abspath(
                        "Imagesknown\Image"+str(noOfFile1)+".jpg")
                    insertImage(Id, pathKnown, "Known")

            else:
                Id = 'Unknown'
                tt = str(Id)
            if(conf > 75):
                unknownimg = unknownimg+1
                if(knownimg <= 1):
                    noOfFile = len(os.listdir("ImagesUnknown"))+1
                    cv2.imwrite("ImagesUnknown\Image" +
                                str(noOfFile) + ".jpg", im[y:y+h, x:x+w])
                    pathUnknown = os.path.abspath(
                        "ImagesUnknown\Image" + str(noOfFile) + ".jpg")
                    insertImage(Id, pathUnknown, "Unknown")

            #cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)
            cv2.putText(im, str(tt), (x+5, y-5), font, 1, (255, 255, 255), 2)
            cv2.putText(im, str(conf), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour, Minute, Second = timeStamp.split(":")
    #fileName = "User_Log\\UserLog_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    #attendance.to_csv(fileName, index=False)
    for i, row in attendance.iterrows():
        insertUserLog(row.Id, row.Name[0], row.Date, row.Time)
    cam.release()
    cv2.destroyAllWindows()
    # print(attendance)
    res = attendance
    message2.configure(text=res)


# clearButton = tk.Button(window, text="Clear", command=clear, fg="black", bg="light slate grey",
 #                       width=10, height=1, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
# clearButton.grid(row=1, column=2, sticky="W", padx=10,
    #   pady=10)
clearButton2 = tk.Button(window, text="Clear", command=clear2, fg="black", bg="light slate grey",
                         width=10, height=1, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
clearButton2.grid(row=2, column=2, sticky="W", padx=10,
                  pady=10)

takeImg = tk.Button(frame, text="Take Images", command=TakeImages, fg="black", bg="light slate grey",
                    width=20, height=1, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
takeImg.grid(row=6, column=2, pady=10)


trainImg = tk.Button(frame, text="Train Images", command=TrainImages, fg="black",
                     bg="light slate grey", width=20, height=1, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
trainImg.grid(row=6, column=3, pady=10, sticky="W")


trackImg = tk.Button(frame, text="Track Images", command=TrackImages, fg="black",
                     bg="light slate grey", width=40, height=1, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")
trackImg.grid(row=7, column=0, columnspan=4, padx=30,
              pady=10)


quitWindow = tk.Button(frame, text="Quit", command=window.destroy, fg="black", bg="light slate grey",
                       width=20, height=2, activebackground="azure", font=('times', 13, ' bold '), borderwidth=3, relief="groove")


quitWindow.grid(row=8, column=1, padx=10, pady=10, columnspan=4)
copyWrite = tk.Text(window, background=window.cget(
    "background"), borderwidth=0, font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
copyWrite.place(x=800, y=750)


window.mainloop()
