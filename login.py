import sqlite3

conn = sqlite3.connect('login.db')
cursor = conn.cursor()

# Step 2: Write Python code to interact with the database
def insert_user(username, password, age, email):
    cursor.execute('''
        INSERT INTO users (username, password, age, email)
        VALUES (?, ?, ?, ?)
    ''', (username, password, age, email))
    conn.commit()

def get_all_users():
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

# You can add more functions for updating, deleting, or querying specific users

@app.route('/add_user', methods=['POST'])
def add_user():
    # Get user data from the form
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    email = request.form['email']

    # Insert the user into the database
    insert_user(username, password, age, email)

    # Redirect back to the index page
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
