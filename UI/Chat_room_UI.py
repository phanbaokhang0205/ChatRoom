import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageDraw, ImageOps

WINDOW_WIDTH = 1700-600
WINDW_HEIGHT = 1111-500
WINDOW_POSITION = '+350+100'

GREY = '#545252'
CYAN = '#BCEEF9'
BLACK = '#2B2B2B'
LIGHT_BLACK = '#353535'

"""
Hàm làm tròn hình ảnh, Em Huy có tìm được cách làm tròn nào 
thì thay giúp e Khang với nghee...
"""


def create_rounded_image(image_path, size):
    # Mở ảnh gốc
    image = Image.open(image_path).convert("RGBA")

    # Thay đổi kích thước ảnh với bộ lọc LANCZOS để giữ chất lượng cao
    image = image.resize((size, size), Image.LANCZOS)

    # Tạo một mặt nạ hình tròn
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)

    # Áp dụng mặt nạ vào ảnh để bo tròn
    rounded_image = ImageOps.fit(image, (size, size), centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    return rounded_image


# 1: container
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # config window
        self.title("Chat room")
        self.geometry(f'{WINDOW_WIDTH}x{WINDW_HEIGHT}{WINDOW_POSITION}')
        self.resizable(False, False)

        # Chia ra 3 Cột 1 Dòng
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

# 2: Frame ben trai.


class LeftFrame(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color="#2B2B2B", corner_radius=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="snew")

# 2.1: Frame:


class LeftTitle(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=BLACK)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.app_name = ctk.CTkLabel(
            master=self,
            text='CHATS',
            font=("Arial", 25, 'bold'),
            text_color=CYAN,
            bg_color=BLACK,
        )
        self.app_name.grid(row=0, column=0, sticky='wsn')

        new_src = Image.open("icons/new.png")
        new_img = ctk.CTkImage(new_src)

        self.new_icon = ctk.CTkButton(
            master=self,
            image=new_img,
            text='',
            bg_color=BLACK,
            fg_color=BLACK,
            height=43, width=43
        )
        self.new_icon.grid(row=0, column=1, sticky='e')

        # Entry search
        search_value = ctk.StringVar()
        self.search_input = ctk.CTkEntry(
            master=self,
            textvariable=search_value,
            border_width=0,
            fg_color=GREY,
            text_color='white'

        )
        self.search_input.grid(row=1, columnspan=2, sticky='snew', pady=10)

        self.grid(row=0, column=0, sticky='snew', padx=(15, 10), pady=(5, 0))

# 2.1.1: Frame user


class UserFrame(ctk.CTkFrame):
    def __init__(self, container, user_img, user_name, content_msg, row):
        super().__init__(container, fg_color=BLACK)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # avatar
        avatar_src = create_rounded_image(user_img, 40)
        new_img = ctk.CTkImage(dark_image=avatar_src, size=(40, 40))

        self.avatar = ctk.CTkLabel(
            master=self,
            text='',
            image=new_img,

        )
        self.avatar.grid(row=0, column=0, sticky='w', rowspan=2, pady=12)

        # user_name
        self.user_name = ctk.CTkLabel(
            master=self,
            text=user_name,
            text_color='white',
            font=("Arial", 14, 'bold')

        )
        self.user_name.grid(row=0, column=1, sticky='w')
        # message_content
        self.pre_content = ctk.CTkLabel(
            master=self,
            text=content_msg,
            text_color='white',
            font=("Arial", 14)

        )
        self.pre_content.grid(row=1, column=1, sticky='w',)

        self.grid(row=row, column=0, sticky='snew', columnspan=2)

# 3: Frame o giua.


class CenterFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=BLACK, corner_radius=0)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        self.grid(row=0, column=1, sticky="snew")

# 3.1 Frame chua tieu de (frame tren cung cua center frame):


class CenterTitle(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=BLACK, corner_radius=0)

        # avatar
        avatar_src = create_rounded_image('img/khang.JPG', 50)
        new_img = ctk.CTkImage(dark_image=avatar_src, size=(50, 50))

        self.avatar = ctk.CTkLabel(
            master=self,
            text='',
            image=new_img,
        ).pack(anchor='w', side='left')
        self.name_content = Name_Content(self, "Phan Bao Khang", 14)
        self.name_content.pack(anchor='w', side='left', padx=(10, 0))

        # Phone & Video icons
        self.icons = Icons_of_CenterTitle(self)
        self.icons.pack(anchor='e', expand=True)

        self.grid(row=0, column=0, sticky='snew', padx=10, pady=0)


class Name_Content(ctk.CTkFrame):
    def __init__(self, container, userName, size):
        super().__init__(container, fg_color=BLACK, corner_radius=0)

        self.name = ctk.CTkLabel(
            master=self,
            text=userName,
            text_color='white',
            font=('Arial', size, 'bold'),
        ).pack(anchor='w')
        self.active = ctk.CTkLabel(
            master=self,
            text="Active now",
            text_color='white',
            font=('Arial', size),
        ).pack(anchor='w')


class Icons_of_CenterTitle(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=BLACK, bg_color=BLACK, corner_radius=0)

        # phone icon
        phone_src = Image.open("icons/phone.png")
        phone_icons = ctk.CTkImage(phone_src)

        # video call icon
        video_src = Image.open("icons/video.png")
        video_icons = ctk.CTkImage(video_src)

        self.phone_icon = ctk.CTkButton(
            master=self,
            image=phone_icons,
            text='',
            bg_color=BLACK,
            fg_color=BLACK,
            width=43
        ).pack(anchor='e', side='left')

        self.video_icon = ctk.CTkButton(
            master=self,
            image=video_icons,
            text='',
            bg_color=BLACK,
            fg_color=BLACK,
            width=43
        ).pack(anchor='e')


# 3.1: Frame chua doan tin nhan.
class MessageTextFrame(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, corner_radius=0)

        self.grid(row=1, column=0, sticky='snew')


# 3.2: Frame chua soan tin nhan.
class InputFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, corner_radius=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)

        self.message = ctk.StringVar()

        # icons
        self.icons = Icons_Of_Input(self)
        self.icons.grid(column=0, padx=0)

        # Input
        self.input = ctk.CTkEntry(
            master=self,
            textvariable=self.message,
            border_width=0,
            height=30,
            fg_color='#D9D9D9',
            text_color=BLACK
        )
        self.input.grid(column=1, row=0, sticky='ew')

        # send button
        send_src = Image.open('icons/send.png')
        send_icons = ctk.CTkImage(send_src)
        self.send_btn = ctk.CTkButton(
            master=self,
            text='',
            image=send_icons,
            fg_color=LIGHT_BLACK,
            width=0,
        )
        self.send_btn.grid(column=2, row=0)

        self.grid(row=2, column=0, sticky='snew', padx=0)


class Icons_Of_Input(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, bg_color=LIGHT_BLACK)

        self.rowconfigure(0, weight=1)

        image_scr = Image.open("icons/image.png")
        mic_scr = Image.open('icons/mic.png')
        eye_scr = Image.open('icons/eye.png')

        image_icon = ctk.CTkImage(image_scr)
        mic_icon = ctk.CTkImage(mic_scr)
        eye_icon = ctk.CTkImage(eye_scr)

        self.image_icon = ctk.CTkButton(
            master=self,
            image=image_icon,
            text='',
            bg_color=LIGHT_BLACK,
            fg_color=LIGHT_BLACK,
            width=5
        ).grid(row=0, column=0)
        self.mic_icon = ctk.CTkButton(
            master=self,
            image=mic_icon,
            text='',
            bg_color=LIGHT_BLACK,
            fg_color=LIGHT_BLACK,
            width=5
        ).grid(row=0, column=1)
        self.eye_icon = ctk.CTkButton(
            master=self,
            image=eye_icon,
            text='',
            bg_color=LIGHT_BLACK,
            fg_color=LIGHT_BLACK,
            width=5
        ).grid(row=0, column=2)


# 4: Frame ben phai
class RightFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, bg_color=LIGHT_BLACK,
                         fg_color=LIGHT_BLACK, corner_radius=0)

        # avatar
        avatar_src = create_rounded_image('img/khang.JPG', 60)
        new_img = ctk.CTkImage(dark_image=avatar_src, size=(60, 60))

        # Avatar
        self.avatar = ctk.CTkLabel(
            master=self,
            text='',
            image=new_img,
        )
        self.avatar.pack(pady=(20, 10))

        # Name & active
        self.name = ctk.CTkLabel(
            master=self,
            text='Phan Bao Khang',
            font=('Arial', 16, 'bold'),
            text_color='white'
        ).pack()
        self.active = ctk.CTkLabel(
            master=self,
            text='Active',
            font=('Arial', 14),
            text_color='white'
        ).pack()

        # icons
        self.icons = Icon_of_Right(self)
        self.icons.pack(pady=10)

        # The buttons
        self.change_emoji = ctk.CTkButton(
            master=self,
            text='Change Emoji',
            width=180,
            height=40,
        )
        self.edit_nickname = ctk.CTkButton(
            master=self,
            text='Edit nicknames',
            width=180,
            height=40,
        )
        self.media = ctk.CTkButton(
            master=self,
            text='Media',
            width=180,
            height=40,
        )
        self.files = ctk.CTkButton(
            master=self,
            text='Files',
            width=180,
            height=40,
        )
        self.change_emoji.pack(pady=10)
        self.edit_nickname.pack()
        self.media.pack(pady=10)
        self.files.pack()
        self.grid(row=0, column=2, sticky="snew")


class Icon_of_Right(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, corner_radius=0)

        volume_off = Image.open('icons/volume_off.png')
        search = Image.open('icons/search.png')

        volume_icon = ctk.CTkImage(volume_off)
        search_icon = ctk.CTkImage(search)

        self.volume_icon = ctk.CTkButton(
            master=self,
            image=volume_icon,
            text='',
            bg_color=LIGHT_BLACK,
            fg_color=LIGHT_BLACK,
            width=43
        ).pack(anchor='e', side='left')

        self.search_icon = ctk.CTkButton(
            master=self,
            image=search_icon,
            text='',
            bg_color=LIGHT_BLACK,
            fg_color=LIGHT_BLACK,
            width=43
        ).pack(anchor='e')


users = [
    {
        'img': 'img/khang.JPG',
        'name': 'Phan Bao Khang',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 1',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 2',
        'content': 'This is content...'
    }, {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 1',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 2',
        'content': 'This is content...'
    }, {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 1',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 2',
        'content': 'This is content...'
    }, {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 1',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 2',
        'content': 'This is content...'
    }, {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 1',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 2',
        'content': 'This is content...'
    },
    {
        'img': 'img/khang.JPG',
        'name': f'Phan Bao Khang 3',
        'content': 'This is content...'
    }
]

i = 3

if __name__ == "__main__":
    app = App()

    leftFrame = LeftFrame(app)
    leftTitle = LeftTitle(leftFrame)
    for user in users:
        userFrame = UserFrame(
            leftTitle,
            user_img=user.get('img'),
            user_name=user.get('name'),
            content_msg=user.get('content'),
            row=i
        )

        i += 1

    centerFrame = CenterFrame(app)
    centerTitle = CenterTitle(centerFrame)
    msgTextFrame = MessageTextFrame(centerFrame)
    inputFrame = InputFrame(centerFrame)

    rightFrame = RightFrame(app)

    app.mainloop()
