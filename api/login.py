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

# Example usage:
insert_user('JohnDoe', 'john@example.com', 'password123')
all_users = get_all_users()
print(all_users)

# Close the connection when done
conn.close()
