import os
import sys
import email
from click import password_option
from django.apps import AppConfig
from django.forms import FileField
from django.shortcuts import render
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, SelectField, PasswordField, FileField, validators, BooleanField, SubmitField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime

from werkzeug.utils import secure_filename
from main import SabahRaporuComplete
from aksamraporu import AksamRaporuComplete
from ssh_sabahraporu_complete import SSH_sabahraporu_complete


app = Flask(__name__)
app.secret_key = "deneme"
app.config["Excel_attachment"] = "Excel_attachment/"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
#app.config["MYSQL_PASSWORD"] = "o26@FfSK29eppX*3"
app.config["MYSQL_DB"] = "ya_rpa"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

# Kullanıcı Giriş Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görmek için lütfen giriş yapın", "danger")
            return redirect(url_for("login"))
    return decorated_function

# Login Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı", render_kw={"style": "border-radius: 10px; width:250px"})
    password = PasswordField("Şifre", render_kw={"style": "border-radius: 10px; width:250px"})

# Login Sayfası
@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        query = "Select * from users1 where username = '{}'"
        result = cursor.execute(query.format(username))
        if result >> 0:
            data = cursor.fetchone()
            real_password_sha = data["password"]
            if sha256_crypt.verify(password_entered, real_password_sha):
                session["logged_in"] = True
                session["username"] = data["username"]
                session["name"] = data["name"]
                session["email"] = data["email"]
                session["surname"] = data["surname"]
                session["departman"] = data["departman"]
                #session["OneriDegerlendirmeYetki"] = data["OneriDegerlendirmeYetki"]
                #session["ProjelendirmeYetki"] = data["ProjelendirmeYetki"]
                flash("Başarıyla giriş yapıldı", "success")
                return redirect(url_for("index"))
            else:
                flash("Kullanıcı Adı veya Şifre hatalı!", "danger")
                return redirect(url_for("login"))
        else:
            flash("Kullanıcı ismi geçersiz!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html", form = form)

# Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("İsim", validators = [validators.Length(min = 2, max = 25)])
    surname = StringField("Soyisim", validators = [validators.Length(min = 2, max = 25)])
    username = StringField("Kullanıcı Adı", validators = [validators.Length(min = 2, max = 30)])
    email = StringField("Email Adresi", validators = [validators.Email(message = "Lütfen Geçerli bir email adresi giriniz.")])
    password = PasswordField("Şifre:", validators=[validators.DataRequired(message = "Lütfen şifre giriniz."), validators.EqualTo(fieldname = "confirm", message = "Şifreniz uyuşmuyor.")])
    confirm = PasswordField("Şifre Doğrulama")
    department = SelectField('Departman', choices=[('Bilgi Teknolojileri', 'Bilgi Teknolojileri'), ('Satış', 'Satış'), ('SSH', 'SSH'), ('Strateji ve Planlama', 'Strateji ve Planlama'), ('İş Geliştirme', 'İş Geliştirme')])

# Kullanıcı Kayıt Sayfası
@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        surname = form.surname.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(form.password.data)
        department = form.department.data

        cursor = mysql.connection.cursor()
        check_query = 'SELECT username FROM users1 where username="{}"'.format(username)
        checked_result = cursor.execute(check_query)
        if checked_result == 0:
            query = 'Insert into users1 (name, surname, username, email, password, departman, adminyetki, superuser) VALUES("{}","{}","{}","{}","{}","{}","{}","{}")'.format(name, surname, username, email, password, department, 0, 0)
            cursor.execute(query)
            mysql.connection.commit()
            cursor.close()
            flash("Başarıyla Kayıt olundu", "success")
            return redirect(url_for("login"))
        else:
            flash("Bu mail adresi ile kayıt açılmış. ", "danger")
            return redirect(url_for("register"))   
    else:
        return render_template("register.html", form=form)

# Anasayfa
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

# Profile Settings
@app.route("/profile&settings", methods = ["GET"])
@login_required
def profileSettings():
    return render_template("profilesettings.html")

# Password Change Form
class PasswordChangeForm(Form):
    oldpw = PasswordField("Eski Şifre", validators=[validators.DataRequired(message = "Boş bırakılamaz.")])
    newpw = PasswordField("Yeni Şifre", validators=[validators.Length(min = 5, max = 45), validators.DataRequired(message = "Boş bırakılamaz."), validators.EqualTo(fieldname = "confirm", message = "Yeni şifreniz eşleşmiyor.")])
    confirm = PasswordField("Yeni Şifre Tekrar")

# Password Change
@app.route("/password&change", methods = ["GET", "POST"])
@login_required
def passwordChange():
    form = PasswordChangeForm(request.form)
    if request.method == "POST" and form.validate():
        hash = form.oldpw.data
        cursor = mysql.connection.cursor()
        query = 'SELECT * FROM users1 where username="{}"'.format(session["username"])
        result_pw = cursor.execute(query)
        result_pw = cursor.fetchone()
        verification = sha256_crypt.verify(hash, result_pw["password"])
        if verification == True:
            newpw = sha256_crypt.hash(form.newpw.data)
            update_query = "UPDATE users1 SET password = '{}' WHERE username='{}'".format(newpw, session["username"])
            cursor.execute(update_query)
            mysql.connection.commit()
            cursor.close()
            flash("Şifrenizi başarıyla değiştirdiniz", "success")
            return redirect(url_for("index"))
    return render_template("passwordchange.html", form=form)

# PCL/PDF job formu
class PclPdfForm(Form):
    file1 = FileField('Excel dosyasını yükle', validators=[FileRequired()])
    dosya_adi = StringField("Oluşturulacak Dosya Adı", render_kw={'style': 'width: 42ch; border-radius:10px; border-color:black;'})
    submit = SubmitField('Upload')

# PCL/PDF job
@app.route("/planlama_pcl_pdf", methods = ["GET", "POST"])
@login_required
def PclPdfJob():
    from pcl_pdf_excel_funcs import read_column_to_list

    form = PclPdfForm(request.form)
    if request.method == "POST":
        file1 = form.file1.data
        dosya_adi = form.dosya_adi.data
        
        file1 = request.files['file1']

        if file1:  # Check if a file was uploaded
            filename = secure_filename(file1.filename)
            file1.save(os.path.join('templates', 'Excel_attachment', filename))
            try:
                values_to_be_searched = read_column_to_list("templates\Excel_attachment" + r"\ ".replace(" ","") + filename)
            except:
                flash("Excel Dosyasını okurken bir hata oluştu.", "danger")
                return redirect(url_for("index"))
            
            values = []
            for value in values_to_be_searched:
                values.append(str(value))
            
            faulty_input_list = [] # The list of input values that are not "FaturaNo" or "ŞasiNo"
            correct_inputs_list = [] # Inputs that have 8 or 17 length, correct format

            for value in values:
                if len(value) == 8 or len(value) == 17:
                    correct_inputs_list.append(value)
                else:
                    faulty_input_list.append(value)

            correct_inputs_length = len(correct_inputs_list)
            faulty_inputs_length = len(faulty_input_list)
            total_inputs_length = len(correct_inputs_list) + len(faulty_input_list)
            
            

            


            flash("Başarılı", "success")
            return redirect(url_for("index"))
        
        else:
            flash("Hata oluştu", "danger")
            return redirect(url_for("index"))
        
    elif request.method == "GET":
        return render_template("planlama_pcl_pdf.html", form=form)
    else:
        return redirect(url_for("index"))

# SSH Sabah Raporu Form
class SSHSabahRaporuForm(Form):
    turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})
    turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})
    first_day_check = BooleanField("Geçen ay kümüle rapor", render_kw={'style': 'width: 30ch; border-color:black;'})

# SSH Sabah Raporu
@app.route("/sshparcaraporu", methods = ["GET", "POST"])
@login_required
def sshparcaraporu():
    form = SSHSabahRaporuForm(request.form)
    if request.method == "POST":
        turkuazusername = form.turkuazusername.data
        turkuazpw = form.turkuazpw.data
        first_day_check = form.first_day_check.data

        SSH_sabahraporu_complete(turkuazusername, turkuazpw, first_day_check)

        flash("Parça Satış Raporu başarıyla gönderildi.", "success")
        return redirect(url_for("index"))

    elif request.method == "GET":
        return render_template("ssh_parcaraporu.html", form=form)

    else:
        return redirect(url_for("sshparcaraporu"))

# Sabah Raporu Form
class SabahRaporuForm(Form):
    turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})
    turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})
    Ithalat = StringField("İthalat adedi", render_kw={'style': 'border-radius:10px; border-color:black;'})
    ToptanFatura = StringField("Toptan Fatura adedi", render_kw={'style': 'border-radius:10px; border-color:black;'})
    Euro_kur = StringField("Euro kuru (ithalat yapıldıysa)", render_kw={'style': 'border-radius:10px; border-color:black;'})

# Sabah Raporu
@app.route("/sabahraporu", methods = ["GET", "POST"])
@login_required
def sabahRaporu():
    form = SabahRaporuForm(request.form)
    if request.method == "POST":
        turkuazusername = form.turkuazusername.data
        turkuazpw = form.turkuazpw.data
        Ithalat = form.Ithalat.data
        ToptanFatura = form.ToptanFatura.data
        Euro_kur = form.Euro_kur.data
        if len(Euro_kur) >= 1:
            pass
        else:
            Euro_kur = None
        SabahRaporuComplete(turkuazusername, turkuazpw, Ithalat, ToptanFatura, Euro_kur)

        flash("Sabah Raporu başarıyla gönderildi.", "success")
        return redirect(url_for("index"))

    elif request.method == "GET":
        return render_template("sabahraporu.html", form=form)

    else:
        return redirect(url_for("sabahraporu"))
    
# Akşam Raporu Form
class AksamRaporuForm(Form):
    turkuazusername = StringField("Turkuaz Kullanıcı Adı", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})
    turkuazpw = PasswordField("Turkuaz Şifre", render_kw={'style': 'width: 30ch; border-radius:10px; border-color:black;'})

# Akşam Raporu
@app.route("/aksamraporu", methods = ["GET", "POST"])
@login_required
def aksamRaporu():
    form = AksamRaporuForm(request.form)
    if request.method == "POST":
        turkuazusername = form.turkuazusername.data
        turkuazpw = form.turkuazpw.data

        AksamRaporuComplete(turkuazusername, turkuazpw) 

        flash("Akşam Raporu başarıyla gönderildi.", "success")
        return redirect(url_for("index"))

    elif request.method == "GET":
        return render_template("aksamraporu.html", form=form)

    else:
        return redirect(url_for("aksamraporu"))

# Logout işlemi
@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış yapıldı","success")
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
