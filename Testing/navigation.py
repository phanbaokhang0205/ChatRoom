import customtkinter as ctk

class TableFrame(ctk.CTkFrame):
    def __init__(self, container, data):
        super().__init__(container)

        # Tạo bảng với dữ liệu từ 'data'
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                cell = ctk.CTkLabel(self, text=value, fg_color="grey", text_color="white")
                cell.grid(row=i, column=j, padx=5, pady=5, ipadx=10, ipady=5, sticky="nsew")

        # Đặt tỉ lệ kích thước cột cho cân đối
        for j in range(len(data[0])):
            self.columnconfigure(j, weight=1)


# Tạo giao diện chính
root = ctk.CTk()
root.geometry("400x300")

# Dữ liệu mẫu để hiển thị trong bảng
data = [
    ["ID", "Name", "Age"],
    ["1", "Alice", "24"],
    ["2", "Bob", "30"],
    ["3", "Charlie", "28"]
]

# Tạo và hiển thị bảng
table_frame = TableFrame(root, data)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
