import customtkinter as ctk
import tkinter as tk

# Khởi tạo cửa sổ chính
root = ctk.CTk()
root.geometry("600x400")

# Frame chính chứa thanh cuộn dọc
scrollable_frame = ctk.CTkScrollableFrame(root, width=500, height=300)
scrollable_frame.grid(row=0, column=0, padx=10, pady=10)

# Khung con bên trong để chứa các widget, sẽ cuộn được cả dọc và ngang
inner_frame = tk.Frame(scrollable_frame)
inner_frame.pack(expand=True, fill="both")

# Thêm các widget vào inner_frame (ví dụ label với nhiều cột)
for i in range(20):
    for j in range(10):
        label = ctk.CTkLabel(inner_frame, text=f"Label {i}-{j}")
        label.grid(row=i, column=j, padx=5, pady=5)

# Tạo thanh cuộn ngang
h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=inner_frame.xview)
h_scrollbar.grid(row=1, column=0, sticky="ew")

# Liên kết scrollbar ngang với canvas của frame
inner_frame.configure(xscrollcommand=h_scrollbar.set)

root.mainloop()
