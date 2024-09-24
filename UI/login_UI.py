import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps
import sqlite3
from tkinter import messagebox
import subprocess


def create_connection():
    try:
        conn = sqlite3.connect('chat_user.db')
        c = conn.cursor()

        c.execute("""
                  CREATE TABLE IF NOT EXISTS users 
                (   id integer primary key, 
                    full_name text not null, 
                    age integer not null, 
                    email text unique, 
                    password INT NOT NULL
                  )""")
        conn.commit()
        print("Connection successed.")
    except sqlite3.Error as e:
        print(f"Connection failed with an error occurred: {e}")

    finally:
        if conn:
            conn.close()


def add_user(name, age, email, password, re_pass):
    if not name.strip() or not email.strip() or not password.strip():
        messagebox.showwarning("Thông báo!", "Bạn phải điền đầy đủ thông tin!")
        return False
    if password != re_pass:
        messagebox.showerror("Thông báo!", "Mật khẩu không trùng khớp")
        return False
    conn = sqlite3.connect('chat_user.db')

    c = conn.cursor()
    c.execute(
        "INSERT INTO users (full_name, age, email, password) VALUES (?, ?, ?, ?)", (name, age, email, password))
    conn.commit()
    print("Added successfully")
    conn.close()
    return True

def check_user(email, password):
    conn = sqlite3.connect('chat_user.db')
    c = conn.cursor()
    c.execute("select * from users where email=? AND password=?",
              (email, password))
    user = c.fetchone()
    conn.close()
    return user is not None


def login_GUI(email, password):
    if check_user(email, password):
        messagebox.showinfo("Thông báo!", "Đăng nhập thành công!")
        app.destroy()
        subprocess.Popen(['python', 'd:/PYTHON/KHANG/ChatRoom/UI/server_UI.py'])
        
    else:
        messagebox.showerror("Thông báo!", "Tài khoản hoặc mật khẩu bị sai!")

def register_GUI(name, age, email, password, re_pass):
    if add_user(name, age, email, password, re_pass):
        messagebox.showinfo("Thông báo!", "Đăng ký tài khoản thành công!")
        goToLogin()
    else:
        messagebox.showerror("Thông báo!", "Đăng ký tài khoản thất bại!")


def printUsers():
    print("users")

def goToRegister():
    login_container.pack_forget()
    register_container.pack(fill='both')

def goToLogin():
    register_container.pack_forget()
    login_container.pack(fill='both')


WINDOW_WIDTH = 1700-600
WINDOW_HEIGHT = 1111-500
WINDOW_POSITION = '+350+100'

GREY = '#545252'
CYAN = '#BCEEF9'
CYAN2 = '#3BD9FC'
BLACK = '#2B2B2B'
LIGHT_BLACK = '#353535'
# 1: container


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # config window
        self.title("Chat room")
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}{WINDOW_POSITION}')
        self.resizable(False, False)


class Login_Container(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.pack(fill='both')


# 2: Left Frame: Login Image


class LeftFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK,
                         fg_color=LIGHT_BLACK)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # image src
        image_src = Image.open('img/lg_3.png')
        image_photo = ctk.CTkImage(
            image_src, size=(WINDOW_WIDTH/2, WINDOW_HEIGHT))

        self.login_image = ctk.CTkLabel(
            master=self,
            text='',
            image=image_photo,
            fg_color=LIGHT_BLACK,

        ).grid(row=0, column=0, sticky='snew', padx=40, pady=40)

        self.grid(row=0, column=0, sticky='snew')


# 3: Right Frame: Login Form
class RightFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK, fg_color=LIGHT_BLACK,
                         corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        underline_font = ctk.CTkFont(family="Arial", size=14, underline=True)

        # Value of input
        self.userValue = ctk.StringVar()
        self.passValue = ctk.StringVar()

        # Title
        self.login_title = ctk.CTkLabel(
            master=self,
            text='LOGIN',
            font=('Aria', 60, 'bold'),
            text_color=CYAN
        ).grid(row=0, column=0, sticky='w', columnspan=2, pady=(120, 40))

        # user or email

        self.user_label = ctk.CTkLabel(
            master=self,
            text='User or Email',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=1, column=0, sticky='w')
        self.user_input = ctk.CTkEntry(
            master=self,
            textvariable=self.userValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY
        )
        self.user_input.grid(row=2, column=0, columnspan=2,
                             sticky='ew', ipady=10, padx=(0, 80), pady=(0, 40))

        # password

        self.pass_label = ctk.CTkLabel(
            master=self,
            text='Password',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=3, column=0, sticky='w')

        # forgot password
        self.pass_label = ctk.CTkButton(
            master=self,
            text='Forgot password?',
            font=underline_font,
            text_color=CYAN2,
            fg_color=LIGHT_BLACK,
            hover_color=LIGHT_BLACK,
            cursor="hand2",
        )
        self.pass_label.grid(row=3, column=1, sticky='e', padx=(0, 75))

        self.pass_input = ctk.CTkEntry(
            master=self,
            textvariable=self.passValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY,
            show='*'
        )
        self.pass_input.grid(row=4, column=0, columnspan=2,
                             sticky='ew', ipady=10, padx=(0, 80), pady=(0, 40))

        # Register_btn
        self.register = ctk.CTkButton(
            master=self,
            text='Create your account ?',
            font=underline_font,
            text_color=CYAN2,
            fg_color=LIGHT_BLACK,
            hover_color=LIGHT_BLACK,
            cursor="hand2",
            command=goToRegister,
        ).grid(row=5, column=0, sticky='w')

        # Login_btn
        self.login_btn = ctk.CTkButton(
            master=self,
            text='Login',
            font=('Aria', 14, 'bold'),
            text_color=BLACK,
            fg_color=CYAN,
            cursor="hand2",
            command=lambda: login_GUI(
                self.user_input.get(), self.pass_input.get()),

        ).grid(row=5, column=1, sticky='e', padx=(0, 80))

        self.grid(row=0, column=1, sticky='snew')


# Register FORM
class Register_Container(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.pack(fill='both')


class Left_Register_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK,
                         fg_color=LIGHT_BLACK)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # image src
        image_src = Image.open('img/lg_3.png')
        image_photo = ctk.CTkImage(
            image_src, size=(WINDOW_WIDTH/2, WINDOW_HEIGHT))

        self.login_image = ctk.CTkLabel(
            master=self,
            text='',
            image=image_photo,
            fg_color=LIGHT_BLACK,

        ).grid(row=0, column=0, sticky='snew', padx=40, pady=40)

        self.grid(row=0, column=0, sticky='snew')


class Right_Register_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK, fg_color=LIGHT_BLACK,
                         corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Value of input
        self.nameValue = ctk.StringVar()
        self.ageValue = ctk.StringVar()
        self.userValue = ctk.StringVar()
        self.passValue = ctk.StringVar()
        self.pass_againValue = ctk.StringVar()

        # Title
        self.login_title = ctk.CTkLabel(
            master=self,
            text='REGISTER',
            font=('Aria', 40, 'bold'),
            text_color=CYAN
        )
        self.login_title.grid(row=0, column=0, sticky='w',
                              columnspan=2, pady=(40, 20))

        # Full name

        self.name_label = ctk.CTkLabel(
            master=self,
            text='Full Name',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=1, column=0, sticky='w')
        self.name_input = ctk.CTkEntry(
            master=self,
            textvariable=self.nameValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY
        )
        self.name_input.grid(row=2, column=0, sticky='ew',
                             ipady=10, padx=(0, 40), pady=(0, 10))

        # Age

        self.age_label = ctk.CTkLabel(
            master=self,
            text='Age',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=1, column=1, sticky='w')
        self.age_input = ctk.CTkEntry(
            master=self,
            textvariable=self.ageValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY
        )
        self.age_input.grid(row=2, column=1, sticky='ew',
                            ipady=10, padx=(0, 40), pady=(0, 10))

        # user or email

        self.user_label = ctk.CTkLabel(
            master=self,
            text='User or Email',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=3, column=0, sticky='w')
        self.user_input = ctk.CTkEntry(
            master=self,
            textvariable=self.userValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY
        )
        self.user_input.grid(row=4, column=0, columnspan=2,
                             sticky='ew', ipady=10, padx=(0, 40), pady=(0, 10))

        # password

        self.pass_label = ctk.CTkLabel(
            master=self,
            text='Password',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=5, column=0, sticky='w')

        self.pass_input = ctk.CTkEntry(
            master=self,
            textvariable=self.passValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY,
            show='*'
        )
        self.pass_input.grid(row=6, column=0, columnspan=2,
                             sticky='ew', ipady=10, padx=(0, 40), pady=(0, 10))

        # password again

        self.pass_label = ctk.CTkLabel(
            master=self,
            text='Password Again',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=7, column=0, sticky='w')

        self.pass_agian_input = ctk.CTkEntry(
            master=self,
            textvariable=self.pass_againValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY,
            show='*'
        )
        self.pass_agian_input.grid(
            row=8, column=0, columnspan=2, sticky='ew', ipady=10, padx=(0, 40), pady=(0, 20))

        # register
        self.register_btn = ctk.CTkButton(
            master=self,
            text='Register',
            font=('Aria', 14, 'bold'),
            text_color=BLACK,
            fg_color=CYAN,
            cursor="hand2",
            command=lambda: register_GUI(self.name_input.get(
            ), self.age_input.get(), self.user_input.get(), self.pass_input.get(), self.pass_agian_input.get())
        ).grid(row=9, column=0, sticky='w', )

        self.grid(row=0, column=1, sticky='snew')


if __name__ == "__main__":
    create_connection()
    app = App()
    login_container = Login_Container(app)
    register_container = Register_Container(app)
    left_register = Left_Register_Frame(register_container)
    right_register = Right_Register_Frame(register_container)

    leftFrame = LeftFrame(login_container)
    rightFrame = RightFrame(login_container)

    app.mainloop()
