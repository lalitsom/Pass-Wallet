import tkinter as tk
main=tk.Tk()
main.configure(background="grey74")
main.geometry("400x200")




def click_enter():
      global frame1,frame2
      frame1.destroy()
      frame2 = tk.LabelFrame (main , text = "PASS-WALLET")
      frame2.pack(fill="x",expand=True)
      tk.Message(frame2, text ="Enter email id", width=125).grid(row = 0,column = 0 )
      tk.Entry(frame2).grid(row = 0 ,column = 1 )
      tk.Message(frame2, text ="Enter password", width=125).grid(row = 1,column = 0 )
      tk.Entry(frame2).grid(row = 1 ,column = 1 )
      Add_Button=tk.Button(main , text="Add", command ="", relief= "raised" )
      Add_Button.place(x=180,y=140)
      Enter_Button.destroy()

frame1 = tk.LabelFrame (main , text = "PASS-WALLET")
frame1.place(relx=0.5,rely=0.5, anchor="center")
tk.Message(frame1, text ="Enter the password to access your wallet", width=125).grid(row = 0,column = 0 )
tk.Entry(frame1).grid(row = 0 ,column = 1 )

Enter_Button=tk.Button(main , text="Enter", command = click_enter, relief= "raised" )
Enter_Button.place(x=180,y=140)





main.mainloop()
