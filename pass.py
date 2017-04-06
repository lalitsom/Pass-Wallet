import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import _thread
import time
import os
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

#functions....................................

local_password =""

def create_files():
    with open("sfile.wallet", "w") as file:
        file.writelines("")
        file.close()
    with open("pfile.wallet", "w") as file:
        file.writelines("")
        file.close()



def check_files():
    if( os.path.isfile('sfile.wallet') and os.path.isfile('pfile.wallet') ):
        print("what")
        Enter_Button.config(command = lambda: click_enter(0))
        init_pass.bind('<Return>', click_enter)
        return True
    else:
        global login_msg
        login_msg.config(text =" Please Create a New Password\n with atleast 5 characters")
        Enter_Button.config(command = lambda: try_create_password(0))
        init_pass.bind('<Return>', try_create_password)
        return False


def create_save_pass(_password):
    m = hashlib.md5()
    m.update(_password)
    with open("pfile.wallet", "w") as file:
        file.writelines(m.hexdigest())
        file.close()


def check_password(_password):
    m = hashlib.md5()
    m.update(_password)
    with open('pfile.wallet', 'r') as content_file:
        content = content_file.read()
        if(m.hexdigest() == content):
            return True
        else:
            return False



def get_saved_file_content():
    if( not os.path.isfile('sfile.wallet') ):
        with open("sfile.wallet", "wb") as file:
            file.writelines("")
            file.close()
    with open('sfile.wallet', 'rb') as content_file:
        content = content_file.read()
        global local_password
        key = get_key(str.encode(local_password))
        f = Fernet(key)
        token = f.decrypt(bytes(content))
        return token

def get_key(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password)
    return base64.urlsafe_b64encode(digest.finalize())



def save_to_file():
    global textarea
    store_data="" + textarea.get('1.0',"end")
    with open("sfile.wallet", "wb") as file:
        global local_password
        key = get_key(str.encode(local_password))
        f = Fernet(key)
        token = f.encrypt(store_data.encode('ascii'))
        #first encrypt then save to file
        file.write(token)



def start_auto_save(_delay,_tmp):
    time.sleep(_delay)
    save_to_file()
    start_auto_save(_delay,0)


def add_margin(_height,_container,_bgcolor):
    margin_name = tk.Label(_container,text="\n",pady=_height,bg=_bgcolor)
    margin_name.pack()


def try_create_password(self):
    global login_frame,text_frame,store_pass,textarea
    check_pass=store_pass.get()
    if (len(check_pass)>=5):
        global local_password
        local_password = check_pass
        create_files()
        create_save_pass( str.encode(check_pass) )
        login_frame.destroy()
        main_window.geometry("500x500")

        text_frame = tk.Frame(main_window, height="500", width="500", bg="#282c34")
        text_frame.pack_propagate(0)

        text_frame.pack(fill="x",expand=False)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        textarea=tk.Text(text_frame,yscrollcommand=scrollbar.set,bg="#f9fbfd",fg="black",font=("Arial","10"))
        textarea.pack(fill="both",expand=True)
        #textarea.insert('1.0',get_saved_file_content())
        textarea.focus()

        scrollbar.config(command=textarea.yview)

        _thread.start_new_thread( start_auto_save,(1,0))
        Enter_Button.destroy()



def click_enter(self):
      global login_frame,text_frame,store_pass,textarea
      check_pass=store_pass.get()

      if (check_password( str.encode(check_pass) )):
          global local_password
          local_password = check_pass
          login_frame.destroy()
          main_window.geometry("500x500")

          text_frame = tk.Frame(main_window, height="500", width="500", bg="#282c34")
          text_frame.pack_propagate(0)

          text_frame.pack(fill="x",expand=False)
          scrollbar = tk.Scrollbar(text_frame)
          scrollbar.pack(side="right", fill="y")

          textarea=tk.Text(text_frame,yscrollcommand=scrollbar.set,bg="#f9fbfd",fg="black",font=("Arial","10"))
          textarea.pack(fill="both",expand=True)
          textarea.insert('1.0',get_saved_file_content())
          textarea.focus()

          scrollbar.config(command=textarea.yview)

          #Add_Button=tk.Button(main_window , text="Save", command =on_save_click, relief= "raised" )
          #Add_Button.place(x=250,y=440)
          _thread.start_new_thread( start_auto_save,(1,0))
          Enter_Button.destroy()
      else:
          global login_msg
          login_msg.config(text="Retry! Wrong Password",fg="red")


#gui......................

main_window=tk.Tk()   #main_window the root container
main_window.wm_title("Pass-Wallet")
main_window.configure(background="#282c34")
main_window.geometry("300x350")
main_window.resizable(width=False, height =False)



login_frame = tk.Frame(main_window, height="350", width="300", bg="#282c34")
login_frame.pack(fill=None, expand=True)
login_frame.pack_propagate(0)




head_name = tk.Label(login_frame,text="PASS - WALLET",bg="#282c34",fg="white",font=("Arial","16","bold"),pady="50")
head_name.pack()

store_pass= tk.StringVar()
init_pass=tk.Entry(login_frame,show="Ø",textvariable=store_pass, width="35")
init_pass.pack(ipady=5)
init_pass.bind('<Return>', click_enter)  #whenever enterkey is pressed try opening the wallet
init_pass.focus()

add_margin(1,login_frame,"#282c34")

Enter_Button=tk.Button(login_frame , text="Login",  relief= "raised" , bg ="#4285fa",fg="white",font=("Arial","15","bold") )
Enter_Button.pack()
Enter_Button.config(height=1, width=9)

add_margin(1,login_frame,"#282c34")

login_msg = tk.Label(login_frame,text="Please Enter Password",bg="#282c34",fg="green",font=("Arial","10","bold"),pady="50")
login_msg.pack()

check_files()

main_window.mainloop()
