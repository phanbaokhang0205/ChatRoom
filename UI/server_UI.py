import customtkinter as ctk
import threading
import socket
from PIL import Image, ImageDraw, ImageOps

WINDOW_WIDTH = 1700-600
WINDOW_HEIGHT = 1111-500
WINDOW_POSITION = '+350+100'

GREY = '#545252'
CYAN = '#BCEEF9'
CYAN2 = '#3BD9FC'
BLACK = '#2B2B2B'
LIGHT_BLACK = '#353535'


host = '127.0.0.1'
port = 6543

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def addNotification(notification):
    app.after(0, lambda: Noti_Item(app.frames['noti_frame'], notification))


def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            addNotification(f"Message from {message.decode('utf-8')}")
            broadcast(message)
        except:
            break

    # Remove client from lists and notify others
    if client in clients:
        clients.remove(client)
    nickname = nicknames.pop(clients.index(
        client)) if client in clients else "Unknown"
    broadcast(f'{nickname} left the chat!'.encode('utf-8'))
    client.close()


def receive():
    while True:
        client, address = server.accept()
        # print(f'Connected with {str(address)}')
        addNotification(f'Connected with {str(address)}')

        client.send('NAME'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # print(f'Nickname of the client_{len(clients)} is {nickname}')
        addNotification(f'Nickname of the client_{len(clients)} is {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def show_frame(frame_to_show, button_to_config):
    # Ẩn tất cả các frame
    for frame in app.frames.values():
        frame.grid_forget()

    # Hiển thị frame được chọn
    frame_to_show.grid(row=0, column=1, sticky='snew', padx=(0, 30))

    # Reset trạng thái tất cả các button
    for button in app.buttons.values():
        button.configure(fg_color=GREY, text_color='white')
        button.grid_configure(padx=(40, 40))

    # Highlight button được click
    button_to_config.configure(fg_color=CYAN, text_color=BLACK)
    button_to_config.grid_configure(padx=(40, 0))

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
        # Dictionary lưu các frame
        self.frames = {}

    def add_frame(self, name, frame):
        """Hàm để thêm frame vào dictionary"""
        self.frames[name] = frame


class Container(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, width=WINDOW_WIDTH,
                         height=WINDOW_HEIGHT, fg_color=LIGHT_BLACK, bg_color=LIGHT_BLACK)
        self.columnconfigure(0, minsize=300)
        self.columnconfigure(1, minsize=1100)
        self.rowconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky='snew')


# 1: Option Buttons Frame
class Option_Buttons(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, corner_radius=0)
        self.columnconfigure(0, weight=1)

        # Server Title
        self.title = ctk.CTkLabel(
            master=self,
            text="Server",
            font=("Aria", 55, 'bold'),
            text_color=CYAN2
        )
        self.title.grid(row=0, column=0, sticky='snew', padx=20, pady=15)

        # User List Button
        self.noti_btn = option_button_item(
            container=self,
            text="Notification",
            commands=lambda: show_frame(
                app.frames['noti_frame'], self.noti_btn)  # Hiển thị Main_Content
        )
        self.user_list_btn = option_button_item(
            container=self,
            text="User List",
            commands=lambda: show_frame(
                app.frames['user_frame'], self.user_list_btn)  # Hiển thị Main_Content
        )
        self.image_mng = option_button_item(
            container=self,
            text="Image Manager",
            commands=lambda: show_frame(
                app.frames['noti_frame'], self.image_mng)  # Hiển thị Main_Content
        )
        self.file_mng = option_button_item(
            container=self,
            text="Files Manager",
            commands=lambda: show_frame(
                app.frames['noti_frame'], self.file_mng)  # Hiển thị Main_Content
        )
        self.media_mng = option_button_item(
            container=self,
            text="Media Manager",
            commands=lambda: show_frame(
                app.frames['noti_frame', self.media_mng])  # Hiển thị Main_Content
        )

        self.noti_btn.grid(row=1, sticky='ew', padx=(40, 40), pady=(60, 0))
        self.user_list_btn.grid(row=2, sticky='ew', padx=(40, 40), pady=40)
        self.image_mng.grid(row=3, sticky='ew', padx=(40, 40))
        self.file_mng.grid(row=4, sticky='ew', padx=(40, 40), pady=40)
        self.media_mng.grid(row=5, sticky='ew', padx=(40, 40))

        # Lưu các button vào dictionary để quản lý
        app.buttons = {
            'user_list_btn': self.user_list_btn,
            'noti_btn': self.noti_btn,
            'image_mng': self.image_mng,
            'file_mng': self.file_mng,
            'media_mng': self.media_mng
        }

        self.grid(row=0, column=0, sticky='snew')


class option_button_item(ctk.CTkButton):
    def __init__(self, container, commands, text, fg=GREY, tcl='white'):
        super().__init__(container, text=text, font=('Aria', 14, 'bold'),
                         fg_color=fg, text_color=tcl, height=50, corner_radius=0, cursor="hand2", border_color=CYAN, command=commands, hover_color=CYAN)


# ----------------------Noti Frame----------------------------------------------------
class Notification_Frame(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=CYAN, corner_radius=0)

        self.grid(row=0, column=1, sticky='snew', padx=(0, 30))


class Noti_Item(ctk.CTkFrame):
    def __init__(self, container, text):
        super().__init__(container, fg_color=CYAN2, height=35)

        self.columnconfigure(0, minsize=50)
        self.columnconfigure(1, minsize=200)

        noti_src = ctk.CTkImage(Image.open("icons/chat.png")) if text.startswith(
            f"Message from ") else ctk.CTkImage(Image.open("icons/noti.png"))
        self.noti_icon = ctk.CTkLabel(
            master=self,
            text='',
            image=noti_src,
            height=35,
            fg_color=BLACK
        )
        self.noti_icon.grid(row=0, column=0, sticky='snew')
        self.noti = ctk.CTkLabel(
            master=self,
            text=text,
            height=35,
            wraplength=600,
            anchor='w'
        )
        self.noti.grid(row=0, column=1, sticky='w', padx=10)

        self.pack(padx=20, pady=20, ipadx=10, anchor='w')
# ----------------------User Frame----------------------------------------------------


class User_List_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=LIGHT_BLACK, corner_radius=0)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.grid(row=0, column=1, sticky='snew', padx=(0, 30))

# 2.1 Table user list


class Title_Table(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=CYAN, corner_radius=0)
        self.rowconfigure(0, weight=1)
        # Giới hạn kích thước của cột ID và cột tuổi
        # Cột ID có kích thước tối thiểu là 50px
        self.columnconfigure(0, minsize=30)
        # Cột Tuổi (Age) có kích thước tối thiểu là 50px
        self.columnconfigure(2, minsize=30)

        # Cột Tên và Email có thể giãn ra
        self.columnconfigure(1, minsize=450)  # Cột Tên có trọng số lớn hơn
        self.columnconfigure(3, minsize=600)  # Cột Email có trọng số lớn hơn

        self.id_title = title_item(self, "ID", 0)
        self.name_title = title_item(self, "Full name", 1)
        self.age_title = title_item(self, "Age", 2)
        self.email_title = title_item(self, "Email", 3)

        self.grid(row=0, column=0, sticky='snew', pady=(40, 20), padx=0)


class title_item(ctk.CTkLabel):
    def __init__(self, container, text, column):
        super().__init__(container, text=text, font=("Aria", 14, 'bold'))

        self.grid(row=0, column=column, sticky='snew')


users = [
    {
        'name': 'Phan Bao Khang',
        'age': '20',
        'email': 'phanbaokhang0205@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Phan Bao Khang',
        'age': '20',
        'email': 'phanbaokhang0205@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Phan Bao Khang',
        'age': '20',
        'email': 'phanbaokhang0205@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
]


class Content_Table(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=CYAN, height=450, corner_radius=0)
        self.columnconfigure(0, weight=1)

        i = 0

        for user in users:
            user_infor_item(
                self, i, i +
                1, user.get('name'), user.get('age'), user.get('email')
            )
            i += 1

        self.grid(row=1, column=0, sticky='snew')


class user_infor_item(ctk.CTkFrame):
    def __init__(self, container, row, id, fullname, age, email):
        super().__init__(container, fg_color=CYAN,)
        self.rowconfigure(0, weight=1)

        # Giới hạn kích thước của cột ID và cột tuổi
        # Cột ID có kích thước tối thiểu là 50px
        self.columnconfigure(0, minsize=30)
        # Cột Tuổi (Age) có kích thước tối thiểu là 50px
        self.columnconfigure(2, minsize=30)

        # Cột Tên và Email có thể giãn ra
        self.columnconfigure(1, minsize=450)  # Cột Tên có trọng số lớn hơn
        self.columnconfigure(3, minsize=600)  # Cột Email có trọng số lớn hơn

        self.id_value = infor_Item(self, id, 0)
        self.name_value = infor_Item(self, fullname, 1)
        self.age_value = infor_Item(self, age, 2)
        self.email_value = infor_Item(self, email, 3)

        self.grid(row=row, column=0, sticky='snew', pady=10)


class infor_Item(ctk.CTkLabel):
    def __init__(self, container, text, column):
        super().__init__(container, text=text, font=("Aria", 14), anchor='center')

        self.grid(row=0, column=column, sticky='snew')


if __name__ == "__main__":
    app = App()
    container = Container(app)

    button_frame = Option_Buttons(container)
    userListFrame = User_List_Frame(container)
    title_table = Title_Table(userListFrame)
    content_table = Content_Table(userListFrame)
    noti_frame = Notification_Frame(container)

    # Thêm frame vào từ điển
    app.add_frame('user_frame', userListFrame)
    app.add_frame('noti_frame', noti_frame)

    # Hiển thị frame chính khi khởi động
    show_frame(app.frames['noti_frame'], button_frame.noti_btn)

    # print('Server is listening...')
    threading.Thread(target=receive, daemon=True).start()
    addNotification('Server is listening...')

    app.mainloop()
