from flask import Flask, render_template, request, redirect, session, url_for, flash
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.secret_key = 'app_secret_key'


def save_user_to_excel(name, email, phone, studytype, password):

    if os.path.exists('users.xlsx'):
        df = pd.read_excel('users.xlsx')
    else:
        df = pd.DataFrame(columns=['name', 'email', 'phone', 'studytype', 'password'])
    
    hashed_password = generate_password_hash(password)
    new_user = pd.DataFrame([[name, email, phone, studytype, hashed_password]], columns=df.columns)
    df = pd.concat([df, new_user], ignore_index=True)
    
    df.to_excel('users.xlsx', index=False)


def verify_user(email, password):
    if os.path.exists('users.xlsx'):
        df = pd.read_excel('users.xlsx')
        user = df[df['email'] == email]
        if not user.empty:
            stored_password = user.iloc[0]['password']
            return check_password_hash(stored_password, password)
    return False


@app.route("/", methods=["GET", "POST"])
def index():
    if 'user' in session:
        return redirect(url_for('account')) 
    return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        rname = request.form['rname']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        studytype = request.form['studytype']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Mật khẩu không khớp. Vui lòng thử lại.')
            return render_template('register.html', rname=rname, name=name, email=email, phone=phone)

        save_user_to_excel(name, email, phone, studytype, password)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if verify_user(email, password):
            flash('Đăng nhập thành công!')
            return redirect(url_for('account'))
        else:
            flash('Email hoặc mật khẩu không đúng. Vui lòng thử lại.')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/account')
def account():
    if 'user' not in session:  # Kiểm tra nếu người dùng chưa đăng nhập
        flash('Bạn phải đăng nhập để truy cập trang này.')
        return redirect(url_for('login'))

    # Lấy email của người dùng từ session
    user_email = session['user']
    return render_template('account.html', user_email=user_email)

# Route đăng xuất
@app.route('/logout')
def logout():
    session.pop('user', None)  # Xóa dữ liệu người dùng khỏi session
    flash('Bạn đã đăng xuất.')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)