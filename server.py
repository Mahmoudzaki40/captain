from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# نقطة نهاية تسجيل المستخدم الجديد
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify(message="Invalid data"), 400
    
    username = data['username']
    password = data['password']
    role = data['role']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()
    return jsonify(message="User registered successfully")

# نقطة نهاية تسجيل الدخول
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify(message="Invalid data"), 400

    username = data['username']
    password = data['password']
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] == password:
        role = result[1]
        return jsonify(message="Login successful", role=role)
    else:
        return jsonify(message="Invalid username or password"), 401

# نقطة نهاية عرض المستخدمين
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify([{"username": user[0], "role": user[1]} for user in users])

# نقطة نهاية حذف المستخدم
@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()
    conn.close()
    return jsonify(success=True)

# نقاط النهاية لجلب الأنظمة الغذائية
@app.route('/diet/weight_loss', methods=['GET'])
def get_weight_loss_diet():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT day, meal1, meal2, meal3, snack, calories FROM weight_loss_diet")
    diet = cursor.fetchall()
    conn.close()
    return jsonify([{"day": row[0], "meal1": row[1], "meal2": row[2], "meal3": row[3], "snack": row[4], "calories": row[5]} for row in diet])

@app.route('/diet/weight_gain', methods=['GET'])
def get_weight_gain_diet():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT day, meal1, meal2, meal3, snack, calories FROM weight_gain_diet")
    diet = cursor.fetchall()
    conn.close()
    return jsonify([{"day": row[0], "meal1": row[1], "meal2": row[2], "meal3": row[3], "snack": row[4], "calories": row[5]} for row in diet])

@app.route('/diet/muscle_cutting', methods=['GET'])
def get_muscle_cutting_diet():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT day, meal1, meal2, meal3, snack, calories FROM muscle_cutting_diet")
    diet = cursor.fetchall()
    conn.close()
    return jsonify([{"day": row[0], "meal1": row[1], "meal2": row[2], "meal3": row[3], "snack": row[4], "calories": row[5]} for row in diet])

@app.route('/diet/muscle_bulking', methods=['GET'])
def get_muscle_bulking_diet():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT day, meal1, meal2, meal3, snack, calories FROM muscle_bulking_diet")
    diet = cursor.fetchall()
    conn.close()
    return jsonify([{"day": row[0], "meal1": row[1], "meal2": row[2], "meal3": row[3], "snack": row[4], "calories": row[5]} for row in diet])

if __name__ == '__main__':
    app.run(debug=True)
