import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageOps

WINDOW_WIDTH = 1700 - 600
WINDOW_HEIGHT = 1111 - 500
WINDOW_POSITION = '+350+100'

GREY = '#545252'
CYAN = '#BCEEF9'
BLACK = '#2B2B2B'
CYAN2 = '#3BD9FC'
LIGHT_BLACK = '#353535'


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # config window
        self.title("Chat room")
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}{WINDOW_POSITION}')
        self.resizable(False, False)

        # Chia ra 3 Cột 1 Dòng
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=9)
        self.rowconfigure(0, weight=1)


class LeftFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white', corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        # Title
        chat_logo = ctk.CTkImage(
            Image.open('img/chatting.png'),
            size=(200, 200)
        )
        self.app_name = ctk.CTkLabel(
            master=self,
            text='',
            image=chat_logo,
            bg_color='white',
        )
        self.app_name.grid(row=0, column=0, columnspan=2,
                           sticky=ctk.EW, pady=(0, 0))

        # Options
        self.option_frame = Option_Frame(self)

        self.grid(row=0, column=0, sticky=ctk.NSEW)


def Home():
    return

# options frame


class Option_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white')

        self.home = Option_Item(self, 'home.png', 'Home', Home)
        self.about = Option_Item(self, 'about.png', 'About', Home)
        self.service = Option_Item(self, 'service.png', 'Service', Home)
        self.portfolio = Option_Item(self, 'portfolio.png', 'Portfolio', Home)
        self.contact = Option_Item(self, 'contact.png', 'Contact', Home)

        self.grid(row=1, column=0, sticky=ctk.NSEW, pady=(0, 0), padx=(0, 0))

# option item


class Option_Item(ctk.CTkFrame):
    def __init__(self, container, icons_src, text, event):
        super().__init__(container, width=100, fg_color='transparent')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)

        icon = ctk.CTkImage(
            Image.open(f'icons/{icons_src}')
        )
        self.image = ctk.CTkLabel(
            master=self,
            text='',
            image=icon,
        )
        self.button = ctk.CTkButton(
            master=self,
            text=text,
            command=event,
            font=("Arial", 14, 'bold'),
            fg_color='transparent',
            text_color=BLACK,
            hover=CYAN,
            anchor=ctk.W,
            width=80
        )
        self.image.grid(row=0, column=0, sticky=ctk.W, padx=(0, 10))
        self.button.grid(row=0, column=1, sticky=ctk.W)

        # Tạo đường phân cách ngang (horizontal separator)
        separator = ctk.CTkFrame(self, height=2, width=120, fg_color="gray")
        separator.grid(row=1, column=0, columnspan=2, sticky=ctk.W)
        self.pack(pady=15)
        


class RightFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='lightgray', corner_radius=0)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.user_infor = User_Infor_Frame(
            self, "Khang Phan",
            "Web developer",
            "Web development has undergone significant changes over the years, evolving from static HTML pages to complex, dynamic web applications. Modern web development combines front-end technologies like...",
            Home)
        self.user_image = User_Img_Frame(
            self, 'user.png'
        )
        self.grid(row=0, column=1, sticky=ctk.NS)


class User_Infor_Frame(ctk.CTkFrame):
    def __init__(self, container, username, job, desc, event):
        super().__init__(container, fg_color='transparent')
        self.columnconfigure(0, weight=1)
        self.h1 = ctk.CTkLabel(
            master=self,
            text=f"Hello, my name is {username}",
            font=("Times", 18, 'bold')
        )
        self.h2 = ctk.CTkLabel(
            master=self,
            text=f"I'm a {job}",
            font=("Times", 18, 'bold')
        )
        self.desc = ctk.CTkLabel(
            master=self,
            text=desc,
            wraplength=450,
            justify="left",
            font=("Times", 18)

        )
        self.button = ctk.CTkButton(
            master=self,
            text='More about me',
            command=event,
        )

        self.h1.grid(row=0, column=0, sticky=ctk.W)
        self.h2.grid(row=1, column=0, sticky=ctk.W, pady=10)
        self.desc.grid(row=2, column=0, sticky=ctk.W, pady=(0, 20))
        self.button.grid(row=3, column=0, sticky=ctk.W)

        self.grid(row=0, column=0, sticky=ctk.W, padx=30)


class User_Img_Frame(ctk.CTkFrame):
    def __init__(self, container, user_img):
        super().__init__(container, fg_color='transparent')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        self.rowconfigure(2,weight=1)
        user_img = ctk.CTkImage(
            Image.open(f'img/{user_img}'),
            size=(300, 300)
        )
        self.image = ctk.CTkLabel(
            master=self,
            text='',
            image=user_img,
            fg_color=CYAN,
        ).grid(row=1, column=1, padx=15)
        self.s1 = ctk.CTkFrame(
            self,height=15,fg_color=CYAN2,corner_radius=5
        ).grid(row=0,column=0, columnspan=2, sticky=ctk.EW)
        self.s2 = ctk.CTkFrame(
            self,height=15,fg_color=CYAN2,corner_radius=5
        ).grid(row=2,column=0, columnspan=2, sticky=ctk.EW)
        self.grid(row=0, column=1, padx=(0, 40), pady=(0,0))


if __name__ == "__main__":
    app = App()
    left_frame = LeftFrame(app)
    right_frame = RightFrame(app)

    app.mainloop()
