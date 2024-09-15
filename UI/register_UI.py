import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps

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

        # Chia ra 2 Cột 1 Dòng
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

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

        ).grid(row=0, column=0, sticky='snew',padx=40, pady=40)

        self.grid(row=0, column=0, sticky='snew')


# 3: Right Frame: Login Form


class RightFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK, fg_color=LIGHT_BLACK,
                         corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        # Title
        self.login_title = ctk.CTkLabel(
            master=self,
            text='Register',
            font=('Aria', 60, 'bold'),
            text_color=CYAN
        ).grid(row=0, column=0, sticky='w', columnspan=2, pady=(80,40))

        # user or email
        self.userValue = ctk.StringVar()

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
        ).grid(row=2, column=0, columnspan=2, sticky='ew', ipady=10, padx=(0, 40), pady=(0,40))

        # password
        self.passValue = ctk.StringVar()

        self.pass_label = ctk.CTkLabel(
            master=self,
            text='Password',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=3, column=0, sticky='w')

        self.pass_input = ctk.CTkEntry(
            master=self,
            textvariable=self.passValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY,
            show='*'
        ).grid(row=4, column=0, columnspan=2, sticky='ew', ipady=10, padx=(0, 40), pady=(0, 40))

        # password again
        self.pass_againValue = ctk.StringVar()

        self.pass_label = ctk.CTkLabel(
            master=self,
            text='Password Again',
            font=('Aria', 14),
            text_color=CYAN
        ).grid(row=5, column=0, sticky='w')

        self.pass_input = ctk.CTkEntry(
            master=self,
            textvariable=self.pass_againValue,
            text_color='white',
            fg_color=GREY,
            border_color=GREY,
            show='*'
        ).grid(row=6, column=0, columnspan=2, sticky='ew', ipady=10, padx=(0, 40), pady=(0, 40))

        # register
        self.register_btn = ctk.CTkButton(
            master=self,
            text='Register',
            font=('Aria',14,'bold'),
            text_color=BLACK,
            fg_color=CYAN,
            cursor="hand2",

        ).grid(row=7, column=0, sticky='w', )

        self.grid(row=0, column=1, sticky='snew')


if __name__ == "__main__":
    app = App()

    leftFrame = LeftFrame(app)
    rightFrame = RightFrame(app)

    app.mainloop()
