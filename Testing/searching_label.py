import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps


class Searching_Label(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, border_width=2, fg_color='transparent', corner_radius=40)
        icon_src = ctk.CTkImage(
            Image.open('icons/search.png'),
            size=(30,30)
        )
        icon_search = ctk.CTkLabel(
            master=self,
            text='',
            image=icon_src
        )
        icon_search.pack(anchor='w',side='left', padx=(10,10))

        search_input = ctk.CTkEntry(
            master=self,
            placeholder_text='Searching something ...',
            border_width=0,
            fg_color='transparent',
            width=250
        )
        search_input.pack(expand=True, anchor='w', padx=(0,15), pady=5)

