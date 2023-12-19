from flask import *
from flask_session import Session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'anishyadav'
app.config['MYSQL_DATABASE_DB'] = 'users_db'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
mysql = MySQL(app)

Session(app)
# Login Page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("use users_db")
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session["name"] = user
            return redirect(url_for('dash'))
        else:
            return 'Invalid username/password combination'
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("use users_db")
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/dash', methods=['GET', 'POST'])
def dash():
    if not session.get("name"):
        return redirect("/")
    return render_template('dash.html')

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    if request.method == 'POST':
        mail = request.form['mail']
        subject = request.form['subject']
        message = request.form['message']

        cur = mysql.connection.cursor()
        cur.execute("use users_db")
        cur.execute("INSERT INTO contact (mail, subject, message) VALUES (%s, %s, %s)", (mail, subject, message))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template("contactus.html")

@app.route('/logout')
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
