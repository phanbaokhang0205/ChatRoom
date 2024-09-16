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
        self.title("Chat room Server")
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}{WINDOW_POSITION}')
        self.resizable(False, False)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class Container(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT, fg_color=LIGHT_BLACK, bg_color=LIGHT_BLACK)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0,weight=1)

        self.grid(row=0, column=0, sticky='snew')




# 1: Option Buttons Frame
class Option_Buttons(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='red')
        self.columnconfigure(0, weight=1)

        # Server Title
        self.title = ctk.CTkLabel(
            master=self,
            text="Server",
            font=("Arial", 60, 'bold')
        )
        self.title.grid(row=0,column=0, sticky='w')


        self.grid(row=0, column=0, sticky='snew')



# 2: Main Content Frame


class Main_Content(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='blue')

        self.grid(row=0, column=1, sticky='snew')


if __name__ == "__main__":
    app = App()
    container = Container(app)

    button_frame = Option_Buttons(container)
    main_content = Main_Content(container)

    app.mainloop()



# # Full name
#         self.fullName = ctk.StringVar()
#         self.fullName_label = ctk.CTkLabel(
#             master=self,
#             text='Full name',
#             font=('Aria', 14),
#             text_color=CYAN
#         ).grid(row=1, column=0, sticky='w')
#         self.fullName_input = ctk.CTkEntry(
#             master=self,
#             textvariable=self.fullName,
#             text_color='white',
#             fg_color=GREY,
#             border_color=GREY
#         )
#         self.fullName_input.grid(row=2, column=0, ipady=5, sticky='w', pady=(0, 30))

#         # Age
#         self.age = ctk.StringVar()
#         self.age_label = ctk.CTkLabel(
#             master=self,
#             text='Age',
#             font=('Aria', 14),
#             text_color=CYAN
#         ).grid(row=1, column=1, sticky='w')
#         self.age_input = ctk.CTkEntry(
#             master=self,
#             textvariable=self.age,
#             text_color='white',
#             fg_color=GREY,
#             border_color=GREY
#         )
#         self.age_input.grid(row=2, column=1, ipady=5, sticky='w', pady=(0, 30))