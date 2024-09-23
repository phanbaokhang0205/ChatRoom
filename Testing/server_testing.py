import customtkinter as ctk
import threading
import socket
from PIL import Image, ImageDraw, ImageOps
from searching_label import Searching_Label

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
    app.after(0, lambda: Noti_Item(noti_frame, notification))


def broadcast(message):
    for client in clients:
        try:

            client.send(message)
        except ConnectionResetError:
            # Nếu client đã ngắt kết nối, loại bỏ khỏi danh sách
            if client in clients:
                clients.remove(client)
            print(f"Client {client} disconnected.")


def handle(client):
    while True:
        try:
            # Nhận dữ liệu từ client
            message = client.recv(4096)

            if not message:
                break

            # Kiểm tra nếu tin nhắn chứa 'IMG' để nhận dữ liệu ảnh
            decoded_message = message.decode('utf-8', errors='ignore')
            if 'IMG' in decoded_message:
                sender_nickname = decoded_message.split(
                    ':')[0]  # Lấy người gửi ảnh

                # Nhận kích thước của ảnh
                img_size_data = client.recv(4)
                img_size = int.from_bytes(img_size_data, byteorder='big')

                # Nhận toàn bộ dữ liệu ảnh
                img_data = b''
                while len(img_data) < img_size:
                    img_data += client.recv(4096)

                # Lưu ảnh vào file (nếu cần)
                with open('received_image_from_client.png', 'wb') as f:
                    f.write(img_data)

                # Gửi ảnh đến tất cả các client khác
                broadcast(f'{sender_nickname}: IMG'.encode(
                    'utf-8'))  # Gửi header 'IMG'
                broadcast(img_size_data)  # Gửi kích thước ảnh
                broadcast(img_data)  # Gửi dữ liệu ảnh

            else:
                # Xử lý tin nhắn văn bản thông thường
                addNotification(f"Message from {decoded_message}")
                broadcast(message)

        except Exception as e:
            print(f'Error occurred: {e}')
            clients.remove(client)
            client.close()
            break

    # Loại bỏ client khỏi danh sách khi ngắt kết nối
    if client in clients:
        clients.remove(client)
    index = clients.index(client) if client in clients else None
    if index is not None:
        nickname = nicknames.pop(index)
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
    frame_to_show.grid(row=0, column=0, sticky=ctk.NSEW, padx=(0, 5))

    # Reset trạng thái tất cả các button
    for button in app.buttons.values():
        button.configure(fg_color='transparent')

    # Highlight button được click
    button_to_config.configure(fg_color='lightgray')

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
        self.rowconfigure(0, minsize=100)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, weight=1)

        self.grid(row=0, column=0, sticky='snew')

# 1: Heading
# 1.1 Icon


class Heading_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white')
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=6)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        self.icon = Icon_Heading(self).grid(
            row=0, column=0, sticky=ctk.W, padx=(10, 0))
        self.search = Searching_Label(self).grid(row=0, column=1, sticky=ctk.W)
        self.buttons = Button_Heading(self).grid(
            row=0, column=2, sticky=ctk.E, padx=(0, 10))

        self.grid(row=0, column=0, sticky=ctk.NSEW,
                  pady=(10), padx=5, columnspan=2)


class Icon_Heading(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, cursor='hand2', fg_color='transparent')

        icon_src = ctk.CTkImage(
            dark_image=Image.open('img/chat.png'),
            size=(50, 50)
        )
        self.icon = ctk.CTkLabel(
            master=self,
            text='',
            image=icon_src
        )
        self.title = ctk.CTkLabel(
            master=self,
            text='Chat Server',
            font=('Arial', 24, 'bold')
        )
        self.icon.pack(side='left', padx=(0, 15))
        self.title.pack(expand=True)

# 1.2 buttons heading


class Button_Heading(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='transparent')

        out_icon = ctk.CTkImage(
            dark_image=Image.open('icons/out.png'),
            size=(30, 30)
        )
        house_icon = ctk.CTkImage(
            dark_image=Image.open('icons/house.png'),
            size=(30, 30)
        )
        self.out_btn = ctk.CTkButton(
            master=self,
            text='Out',
            image=out_icon,
            compound=ctk.LEFT,
            anchor=ctk.W,
            fg_color='transparent',
            text_color=BLACK,
            width=80,
            cursor='hand2',
            hover_color='white'
        )
        self.house_btn = ctk.CTkButton(
            master=self,
            text="Home",
            image=house_icon,
            compound=ctk.LEFT,
            width=100,
            cursor='hand2',
            fg_color='lightgreen',
            text_color=BLACK,
            hover_color='lightgreen'
        )
        self.out_btn.pack(side='left')
        self.house_btn.pack(expand=True)


# 2. left side
class Option_Buttons(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container,  fg_color='transparent')
        noti = ctk.CTkImage(
            dark_image=Image.open('icons/noti.png'),
            size=(30, 30)
        )
        users = ctk.CTkImage(
            dark_image=Image.open('icons/team.png'),
            size=(30, 30)
        )
        files = ctk.CTkImage(
            dark_image=Image.open('icons/folder.png'),
            size=(30, 30)
        )
        images = ctk.CTkImage(
            dark_image=Image.open('icons/gallery.png'),
            size=(30, 30)
        )

        self.noti_btn = ctk.CTkButton(
            master=self,
            text='Notification',
            compound=ctk.TOP,
            font=('Arial', 12, 'bold'),
            image=noti,
            width=80,
            text_color=BLACK,
            cursor='hand2',
            fg_color='transparent',
            hover_color='lightgray',
            command=lambda: show_frame(
                app.frames['noti_frame'], self.noti_btn)
        )
        self.user_btn = ctk.CTkButton(
            master=self,
            text='Users',
            compound=ctk.TOP,
            font=('Arial', 12, 'bold'),
            image=users,
            width=80,
            text_color=BLACK,
            cursor='hand2',
            fg_color='transparent',
            hover_color='lightgray',
            command=lambda: show_frame(
                app.frames['user_frame'], self.user_btn)
        )
        self.file_btn = ctk.CTkButton(
            master=self,
            text='Files',
            compound=ctk.TOP,
            font=('Arial', 12, 'bold'),
            text_color=BLACK,
            image=files,
            width=80,
            cursor='hand2',
            fg_color='transparent',
            hover_color='lightgray',
            command=lambda: show_frame(
                app.frames['noti_frame'], self.file_btn)
        )
        self.img_btn = ctk.CTkButton(
            master=self,
            text='Image',
            compound=ctk.TOP,
            text_color=BLACK,
            font=('Arial', 12, 'bold'),
            image=images,
            width=80,
            cursor='hand2',
            fg_color='transparent',
            hover_color='lightgray',
            command=lambda: show_frame(
                app.frames['noti_frame'], self.img_btn)
        )

        # Lưu các button vào dictionary để quản lý
        app.buttons = {
            'user_list_btn': self.user_btn,
            'noti_btn': self.noti_btn,
            'image_mng': self.img_btn,
            'file_mng': self.file_btn,
        }
        self.noti_btn.pack(expand=True, ipadx=5, ipady=5, pady=(0, 10))
        self.user_btn.pack(expand=True, ipadx=5, padx=10,
                           ipady=5, pady=(0, 10))
        self.file_btn.pack(expand=True, ipadx=5, ipady=5, pady=(0, 10))
        self.img_btn.pack(expand=True, ipadx=5, ipady=5, pady=(0, 10))

        self.pack(pady=(10, 0))


class Button_Side_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white')

        self.grid(row=1, column=0, sticky=ctk.NS, pady=(0, 5), padx=5)

# 3. content


class Main_Content(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='transparent')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.grid(row=1, column=1, sticky=ctk.NSEW, pady=(0, 5), padx=5)


# 3.1 ----------------------Noti Frame----------------------------------------------------
class Noti_Frame(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white')


        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=(0, 5))


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


# 3.2 ----------------------User Frame----------------------------------------------------
class User_Frame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color='white')

        self.title = Title_User(self)
        self.content = Content_Table(self)

        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=(0, 5))

# 2.1 Table user list


class Title_User(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=CYAN2)
        self.rowconfigure(0, weight=1)

        # Giới hạn kích thước của cột ID và cột tuổi
        # Cột ID có kích thước tối thiểu là 50px
        self.columnconfigure(0, weight=1)
        # Cột Tuổi (Age) có kích thước tối thiểu là 50px
        self.columnconfigure(2, minsize=350)

        # Cột Tên và Email có thể giãn ra
        self.columnconfigure(1, weight=1)  # Cột Tên có trọng số lớn hơn
        self.columnconfigure(3, minsize=350)  # Cột Email có trọng số lớn hơn

        self.id_title = title_item(self, "ID", 0)
        self.name_title = title_item(self, "Full name", 1)
        self.age_title = title_item(self, "Age", 2)
        self.email_title = title_item(self, "Email", 3)

        self.pack(side=ctk.TOP, expand=False,
                  fill='x', ipady=10, padx=8, pady=5)


class title_item(ctk.CTkLabel):
    def __init__(self, container, text, column):
        super().__init__(container, text=text, font=("Aria", 14, 'bold'))

        self.grid(row=0, column=column)


class Content_Table(ctk.CTkScrollableFrame):
    def __init__(self, container):
        super().__init__(container, fg_color=CYAN, height=450, corner_radius=10)
        self.columnconfigure(0, weight=1)

        i = 0

        for user in users:
            user_infor_item(
                self, i, i +
                1, user.get('name'), user.get('age'), user.get('email')
            )
            i += 1

        self.pack(expand=True, fill='both', padx=8, pady=5)


class user_infor_item(ctk.CTkFrame):
    def __init__(self, container, row, id, fullname, age, email):
        super().__init__(container, fg_color='white')
        self.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, minsize=300)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, minsize=350)

        self.id_value = infor_Item(self, id, 0)
        self.name_value = infor_Item(self, fullname, 1)
        self.age_value = infor_Item(self, age, 2)
        self.email_value = infor_Item(self, email, 3)

        self.grid(row=row, column=0, sticky='snew', pady=(0, 30))


class infor_Item(ctk.CTkLabel):
    def __init__(self, container, text, column):
        super().__init__(container, text=text, font=("Aria", 14), height=40)

        self.grid(row=0, column=column)


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
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    },
    {
        'name': 'Le Van Quoc Huy',
        'age': '20',
        'email': 'quochuydz@gmail.com',
    }
]


# ----------------------File manager Frame----------------------------------------------------


if __name__ == "__main__":
    app = App()
    con = Container(app)

    heading = Heading_Frame(con)
    side = Button_Side_Frame(con)
    content = Main_Content(con)
    opt_button = Option_Buttons(side)

    noti_frame = Noti_Frame(content)
    user_frame = User_Frame(content)

    # Thêm frame vào từ điển
    app.add_frame('noti_frame', noti_frame)
    app.add_frame('user_frame', user_frame)

    # Hiển thị frame chính khi khởi động
    show_frame(app.frames['noti_frame'], opt_button.noti_btn)

    addNotification('Server is listening...')

    app.mainloop()
