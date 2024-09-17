import customtkinter as ctk
from PIL import Image


root = ctk.CTk()
root.geometry("400x400")

msg = ctk.CTkLabel(
    master=root,
    text="Helloo"
).pack(ipadx=5, ipady=5, pady=10, anchor=ctk.W, side=ctk.RIGHT)

emoji = ctk.CTkButton(
    master=root,
    text="emoji"
).pack()

root.mainloop()
