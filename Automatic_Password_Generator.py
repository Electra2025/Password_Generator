from tkinter import *
from PIL import Image,ImageTk
from tkinter import messagebox
import string
import random
import sqlite3
import datetime
import pyperclip

window = Tk()
window.geometry('1500x1000+0+0')
window.configure(bg='black')
window.title('Automatic Password Generator')

currentDateTime = datetime.datetime.now()

def generate():
    if usernamefield.get() == '':
        messagebox.showerror('','Name cannot be empty')
        return
    
    else:
        Lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        numbers = string.digits
        characters = string.punctuation
        shuffle = Lowercase+uppercase+numbers+characters
        # print(shuffle)

        passwordLength = int(length_box.get())

        if not option.get():
            messagebox.showerror('!','Choose an option')
            return
        elif option == 1:
            passwordfield.insert(0,random.sample(Lowercase,passwordLength))

        elif option == 2:
            passwordfield.insert(0,random.sample(Lowercase+uppercase+numbers,passwordLength))

        elif option == 3:
            passwordfield.insert(0,random.sample(shuffle,passwordLength))
        
        password = random.sample(shuffle,passwordLength)
        passwordfield.insert(0,password)

        con = sqlite3.connect("Automatic_password_gen.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        cur = con.cursor()

        con.execute("CREATE TABLE IF NOT EXISTS password_Generator(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL," \
        "Time_stamp TIMESTAMP)")
        cur.execute("SELECT * FROM password_Generator")
        # print("Table created successfully")
        # con.commit()
        # con.close()
        selectn = ("SELECT * FROM password_Generator WHERE Username = ?")
        cur.execute(selectn, [(usernamefield.get())])
        if cur.fetchone():
            messagebox.showerror('!','This username already exist')
            usernamefield.delete(0,END)
            passwordfield.delete(0,END)
            length_box.delete(0)
            option.set(0)
        else:
            insert = str("INSERT INTO password_Generator(Username,GeneratedPassword,Time_stamp) VALUES(?,?,?)")
            cur.execute(insert,(usernamefield.get(),passwordfield.get(),currentDateTime))
            messagebox.showinfo('Success','Password generator successfully')
            con.commit()
            con.close()

            msg = messagebox.askyesno('','Do you want to clear the fields?')
            if msg:
                option.set(0)
                passwordfield.delete(0,END)
                usernamefield.delete(0,END)
                length_box.delete(0)
                return
            
def copy():
    random_password = passwordfield.get()
    pyperclip.copy(random_password)
    messagebox.showinfo('','Copied')

def reset():
    option.set(0)
    passwordfield.delete(0,END)
    usernamefield.delete(0,END)
    length_box.delete(0,END)


Font = ('arial',15,'bold')

headinglbl = Label(window,text='Automatic Password Generator',font=('times new roman',34,'bold'),bg='black',
                   fg='springgreen2')
headinglbl.grid(pady=18,padx=330)

usernamelbl = Label(window,text='Username:',font=Font,bg='black',fg='white')
usernamelbl.grid(pady=10)

usernamefield = Entry(window,width=25,bd=2,font=Font)
usernamefield.grid(pady=10)

option = IntVar()

strength1 = Radiobutton(window,bg='cyan3',text='Weak Strength',value=1,variable=option,font=Font)
strength1.grid(pady=10)

strength2 = Radiobutton(window,bg='cyan3',text='Medium Strength',value=2,variable=option,font=Font)
strength2.grid(pady=10)

strength3 = Radiobutton(window,bg='cyan3',text='Strong Strength',value=3,variable=option,font=Font)
strength3.grid(pady=10)

passwordLengthlbl = Label(window,text='Password Length',font=Font,bg='black',fg='white')
passwordLengthlbl.grid(pady=10)

length_box = Spinbox(window,from_=6,to=20,width=5,font=Font)
length_box.grid(pady=10)

generatebutton = Button(window,text='Generate',font=Font,highlightbackground='springgreen2',cursor='hand2',command=generate)
generatebutton.grid(pady=10)

passwordfield = Entry(window,width=25,bd=2,font=Font)
passwordfield.grid(pady=10)

copybutton = Button(window,text='Copy',font=Font,highlightbackground='springgreen2',cursor='hand2',command=copy)
copybutton.grid(pady=10)

resetbutton = Button(window,text='Reset',font=Font,highlightbackground='springgreen2',cursor='hand2',command=reset)
resetbutton.grid(pady=6)

usernameImage = PhotoImage(file='password_gen.png')
usernameLabel = Label(window,image=usernameImage)
usernameLabel.place(x=135,y=250)

usernameImage1 = PhotoImage(file='password_gen.png')
usernameLabel1 = Label(window,image=usernameImage)
usernameLabel1.place(x=850,y=250)



window.mainloop()