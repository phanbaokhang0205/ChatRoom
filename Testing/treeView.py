import customtkinter as ctk


WINDOW_WIDTH = 1700-600
WINDOW_HEIGHT = 1111-500
WINDOW_POSITION = '+350+100'

GREY = '#545252'
CYAN = '#BCEEF9'
CYAN2 = '#3BD9FC'
BLACK = '#2B2B2B'
LIGHT_BLACK = '#353535'


app = ctk.CTk(
    fg_color='lightblue'
)
app.geometry(f'1100x611{WINDOW_POSITION}')
app.resizable(False,False)


# left frame
left_frame = ctk.CTkFrame(
    app,fg_color='lightgreen'
) 
lb1 = ctk.CTkLabel(
    left_frame,
    text='Label 1',
    fg_color='green'
)

left_frame.place(relwidth=0.3, relheight=1, relx=0, rely=0)
lb1.pack(fill='x')

# right frame
right_frame = ctk.CTkFrame(
    app,fg_color='lightyellow'
)
id = ctk.CTkLabel(
    right_frame,
    text='ID',
    fg_color='red'
)
fullName = ctk.CTkLabel(
    right_frame,
    text='fullName',
    fg_color='blue'
)
age = ctk.CTkLabel(
    right_frame,
    text='age',
    fg_color='green'
)
email = ctk.CTkLabel(
    right_frame,
    text='email',
    fg_color='pink'
)
right_frame.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
id.place(relx=0,rely=0.3, relwidth=1)
fullName.place(relx=0.1,rely=0.3, relwidth=1)
age.place(relx=0.4,rely=0.3, relwidth=1)
email.place(relx=0.1,rely=0.3, relwidth=1)

app.mainloop()
