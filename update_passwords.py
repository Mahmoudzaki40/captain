import sqlite3
import bcrypt

def update_passwords():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users")
    users = cursor.fetchall()
    
    for user in users:
        username = user[0]
        password = user[1].encode('utf-8')
        
        # Check if the password is already hashed
        if not password.startswith(b'$2b$'):
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            cursor.execute("UPDATE users SET password=? WHERE username=?", (hashed, username))
    
    conn.commit()
    conn.close()

update_passwords()
