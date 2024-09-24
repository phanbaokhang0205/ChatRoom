import sqlite3

try:
    # Tạo kết nối
    conn = sqlite3.connect('user.db')

    # tạo cursor
    c = conn.cursor()

    # tạo bảng
    c.execute(""" CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER) """)

    # chèn dữ liệu
    c.execute("INSERT INTO users (name, age) VALUES ('Alice', 30)")  
    c.execute("INSERT INTO users (name, age) VALUES ('Bob', 25)") 
    # commit lưu thay đổi
    conn.commit()

    # Lấy và in dữ liệu  
    c.execute("SELECT * FROM users")  
    rows = c.fetchall()  

    for row in rows:  
        print(row)  
except sqlite3.Error as e:  
        print(f"An error occurred: {e}")

finally:
    # Đóng kết nối  
    conn.close()  