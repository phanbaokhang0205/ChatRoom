import customtkinter as ctk  

def show_success_message():  
    # Tạo một cửa sổ Toplevel mới để hiển thị thông báo  
    success_window = ctk.CTkToplevel()  
    success_window.title("Thông báo")  
    success_window.geometry("400x150+750+400")  

    # Thêm một label để hiển thị thông báo  
    message_label = ctk.CTkLabel(success_window, text="Đăng ký thành công!")  
    message_label.pack(pady=20)  

    # Thêm một nút để đóng cửa sổ thông báo  
    close_button = ctk.CTkButton(success_window, text="Đóng", command=success_window.destroy)  
    close_button.pack(pady=10)  

# Tạo cửa sổ chính  
app = ctk.CTk()  
app.title("Ứng dụng đăng ký")  
app.geometry("400x300")  

# Giả lập một quy trình đăng ký  
register_button = ctk.CTkButton(app, text="Đăng ký", command=show_success_message)  
register_button.pack(pady=50)  

app.mainloop()