from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2

app = Flask(__name__)

def conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT", 5432)
    )

def create_db():
    conn = conn()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
                   id SERIAL PRIMARY KEY,
                   username VARCHAR(255) NOT NULL,
                   email VARCHAR(255) NOT NULL,
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )

  """)
    conn.commit()
    cursor.close()
    conn.close()
@app.route('/add_user', methods=['POST'])
def create_u():
    db = conn()
    cursor = db.cursor()

    user = request.form['username']
    mail = request.form['email']

    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    cursor.execute(query, (user, mail))
    db.commit()
    cursor.close()
    db.close()  

@app.route('/')
def index():
    con = conn()
    cursor = con.cursor

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    return render_template('users.html', users=rows)

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user_detail(user_id):
    con = conn()
    cursor = con.cursor
    cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        new_username = request.form['username']
        new_email = request.form['email']
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s;", 
                       (new_username, new_email, user_id))
        con.commit()
        return  redirect(url_for('user_detail',user_id = user_id ))
    
    cursor.close()
    con.close()

    if user:
        return render_template('user.html', user=user)
    else:
        return "Usuario no encontrado", 404


@app.route('/delete_user/<int:user_id>',methods=['POST'])
def delete_user(user_id):
    con = conn()
    cursor = con.cursor

    query = "DELETE FROM users Where id = %s;"
    cursor.execute(query, (user_id,))

    con.commit
    cursor.close()
    con.close()

    return redirect(url_for('index'))



if __name__ == "__main__":
    create_db()
