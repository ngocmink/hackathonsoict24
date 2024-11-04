import pandas as pd
import os
from werkzeug.security import generate_password_hash


def save_user_to_excel(name, email, phone, password):
    try:
        if os.path.exists('users.xlsx'):
            df = pd.read_excel('users.xlsx')
        else:
            df = pd.DataFrame(columns=['name', 'email', 'phone', 'password'])
        
        hashed_password = generate_password_hash(password)
        new_user = pd.DataFrame([[name, email, phone, hashed_password]], columns=df.columns)
        df = pd.concat([df, new_user], ignore_index=True)
        
        df.to_excel('users.xlsx', index=False)
        print("Đã lưu thông tin người dùng vào tệp Excel thành công!")
    except Exception as e:
        print("Lỗi khi lưu vào tệp Excel:", e)

# Thử lưu một người dùng mẫu
save_user_to_excel("Alice", "alice@example.com", "123456789", "password123")
