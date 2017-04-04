import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import _thread
import time
import os

#functions....................................

def get_saved_file_content():
    if( not os.path.isfile('sfile.wallet') ):
        with open("sfile.wallet", "w") as file:
            file.writelines("")
            file.close()

    with open('sfile.wallet', 'r') as content_file:
        content = content_file.read()
        #first decrypt then return content
        return content




def save_to_file():
    global textarea
    store_data=textarea.get('1.0',"end")
    with open("sfile.wallet", "w") as file:
        #first encrypt then save to file
        file.writelines(store_data)



def start_auto_save(_delay,_tmp):
    time.sleep(_delay)
    save_to_file()
    start_auto_save(_delay,0)


def add_margin(_height,_container,_bgcolor):
    margin_name = tk.Label(_container,text="\n",pady=_height,bg=_bgcolor)
    margin_name.pack()


def click_enter(self):
      global login_frame,text_frame,store_pass,textarea
      check_pass=store_pass.get()
      if (check_pass=="wp"):
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

Enter_Button=tk.Button(login_frame , text="Login", command = lambda: click_enter(0), relief= "raised" , bg ="#4285fa",fg="white",font=("Arial","15","bold") )
Enter_Button.pack()
Enter_Button.config(height=1, width=9)

add_margin(1,login_frame,"#282c34")

login_msg = tk.Label(login_frame,text="Please Enter Password",bg="#282c34",fg="green",font=("Arial","10","bold"),pady="50")
login_msg.pack()


main_window.mainloop()
