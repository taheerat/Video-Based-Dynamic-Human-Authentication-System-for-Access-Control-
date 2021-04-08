from tkinter import *
import tkinter.font as tkFont
import os
import tkinter as tk

def login_verify():
  
  username1 = username_verify.get()
  password1 = password_verify.get()
  username_entry1.delete(0, END)
  password_entry1.delete(0, END)

  if username1=="admin" and password1=="admin":
      login_sucess()
    
  else:
      user_not_found()

  #list_of_files = os.listdir()
  #if username1 in list_of_files:
    #file1 = open(username1, "r")
    #verify = file1.read().splitlines()
    #if password1 in verify:
        #login_sucess()
    #else:
        #password_not_recognised()

def delete4():
  screen5.destroy()
  
def login_sucess():
  os.system("python train.py")
  


def user_not_found():
  global screen5
  screen5 = Toplevel(screen2)
  screen5.title("Success")
  screen5.geometry("150x100")
  tk.Label(screen5, text = "User Not Found").pack()
  Button(screen5, text = "OK", command =delete4).pack()

global screen2
screen2 = tk.Tk()
screen2.title("Login")
screen2.geometry("1280x720")
tk.Label(screen2, text="Video Based Dynamic Human Authentication System for Access Control",
                   bg="slate grey", fg="white", width=80, height=3, font=('times', 20, ' bold underline'), borderwidth=3, relief="solid").pack()
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
large_font = ('Verdana',30)
small_font = ('Verdana',10)
tk.Label(screen2, text = "Please enter details below to login",font=fontStyle).pack()
tk.Label(screen2, text = "").pack()

global username_verify
global password_verify
  
username_verify = StringVar()
password_verify = StringVar()

global username_entry1
global password_entry1
  

tk.Label(screen2, text = "Username * ",font=fontStyle).pack(fill=BOTH, expand=NO)
username_entry1 = Entry(screen2,font=large_font, textvariable = username_verify)
username_entry1.pack()
tk.Label(screen2, text = "").pack()
tk.Label(screen2, text = "Password * ",font=fontStyle).pack(fill=BOTH, expand=NO)
password_entry1 = Entry(screen2,font=large_font,show='*', textvariable = password_verify)
password_entry1.pack()
tk.Label(screen2, text = "").pack()
Button(screen2, text = "Login",font=fontStyle, width = 10, height = 1, command = login_verify).pack()



  

